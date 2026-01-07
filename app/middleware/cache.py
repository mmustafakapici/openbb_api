"""
Caching middleware for FastAPI.

Implements in-memory caching with optional Redis backend.
"""
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.datastructures import Headers
from typing import Optional, Dict, Any
import hashlib
import json
import time
from functools import wraps
from cachetools import TTLCache

from app.config import settings


class SimpleCache:
    """Simple in-memory cache with TTL support."""

    def __init__(self):
        """Initialize cache."""
        self._cache: TTLCache = TTLCache(maxsize=1000, ttl=300)  # 5 min default

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        return self._cache.get(key)

    def set(self, key: str, value: Any, ttl: int = 300) -> None:
        """Set value in cache with TTL."""
        # Create a new cache entry with specific TTL
        entry = {"value": value, "expires": time.time() + ttl}
        self._cache[key] = entry

    def delete(self, key: str) -> None:
        """Delete value from cache."""
        if key in self._cache:
            del self._cache[key]

    def clear(self) -> None:
        """Clear all cache entries."""
        self._cache.clear()


# Global cache instance
_cache = SimpleCache()


def get_cache() -> SimpleCache:
    """Get cache instance."""
    return _cache


def cache_key_builder(request: Request) -> str:
    """
    Build cache key from request.

    Includes method, path, and query params.
    """
    # Create key from method and path
    key_parts = [
        request.method,
        request.url.path,
        str(sorted(request.query_params.items()))
    ]

    key_string = ":".join(key_parts)
    return f"mobile:{hashlib.md5(key_string.encode()).hexdigest()}"


def cached_response(ttl: int = 300, cache_headers: bool = True):
    """
    Decorator to cache endpoint responses.

    Args:
        ttl: Time to live in seconds
        cache_headers: Whether to add Cache-Control headers
    """

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Try to get from cache
            request = kwargs.get("request") or (
                args[0] if args and isinstance(args[0], Request) else None
            )

            if request:
                cache_key = cache_key_builder(request)
                cached = _cache.get(cache_key)

                if cached is not None:
                    # Check if expired
                    if cached.get("expires", 0) > time.time():
                        response_data = cached["value"]
                        response = Response(
                            content=json.dumps(response_data),
                            media_type="application/json",
                            status_code=200
                        )

                        if cache_headers:
                            response.headers["X-Cache"] = "HIT"
                            response.headers["Cache-Control"] = f"public, max-age={ttl}"

                        return response

            # Call the actual function
            result = await func(*args, **kwargs)

            # Cache the result
            if request and isinstance(result, (dict, list)):
                cache_key = cache_key_builder(request)
                _cache.set(cache_key, result, ttl)

                # Add cache headers to response
                if hasattr(result, "__dict__"):
                    # It's a Pydantic model
                    if cache_headers:
                        # We'll handle this in the response
                        pass

            return result

        return wrapper

    return decorator


class CacheMiddleware(BaseHTTPMiddleware):
    """
    Cache middleware for FastAPI.

    Automatically caches GET requests based on TTL settings.
    """

    def __init__(self, app, cache_get_requests: bool = True):
        """
        Initialize cache middleware.

        Args:
            app: ASGI application
            cache_get_requests: Whether to cache GET requests
        """
        super().__init__(app)
        self.cache_get_requests = cache_get_requests

    async def dispatch(self, request: Request, call_next):
        """Process request with caching."""
        # 1. Skip caching for non-GET or disabled caching
        if request.method != "GET" or not self.cache_get_requests:
            return await call_next(request)

        # 2. Skip documentation and static paths to avoid issues with large streaming responses
        path = request.url.path
        if any(path.startswith(p) for p in ["/docs", "/redoc", "/openapi.json", "/static"]):
            return await call_next(request)

        # 3. Check cache
        cache_key = cache_key_builder(request)
        cached = _cache.get(cache_key)
        if cached and cached.get("expires", 0) > time.time():
            response_data = cached["value"]
            response = Response(
                content=json.dumps(response_data),
                media_type="application/json",
                status_code=200
            )
            response.headers["X-Cache"] = "HIT"
            response.headers["Cache-Control"] = "public, max-age=300"
            return response

        # 4. Process request
        response = await call_next(request)

        # 5. Only try to cache successful JSON responses
        content_type = response.headers.get("content-type", "")
        if response.status_code == 200 and "application/json" in content_type:
            try:
                # Buffer the response body
                body = b""
                async for chunk in response.body_iterator:
                    body += chunk

                # Try to cache it
                try:
                    json_data = json.loads(body.decode())
                    _cache.set(cache_key, json_data, ttl=300)
                except (json.JSONDecodeError, UnicodeDecodeError):
                    pass

                # Re-construct response ALWAYS after consuming body_iterator
                new_response = Response(
                    content=body,
                    status_code=response.status_code,
                    headers=dict(response.headers),
                    media_type=response.media_type
                )
                new_response.headers["X-Cache"] = "MISS"
                return new_response

            except Exception:
                # Fallback to empty response if consumption failed (rare)
                return response

        response.headers["X-Cache"] = "MISS"
        return response
