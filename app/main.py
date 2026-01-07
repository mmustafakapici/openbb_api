"""
OpenBB Mobile API - Main FastAPI Application.

Mobile-optimized REST API for financial data using OpenBB Platform's free providers.
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime
import uvicorn

from app.config import settings
from app.routers import (
    equity_router,
    economy_router,
    regulators_router,
    crypto_router,
    currency_router,
    etf_router,
    extra_providers_router
)
from app.middleware import CacheMiddleware


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    description="""
    Mobile-optimized REST API for financial data using OpenBB Platform.

    ## Features

    * **Lightweight Responses**: Optimized for mobile bandwidth
    * **No API Keys Required**: Uses free providers
    * **Smart Caching**: Multi-level caching for fast responses
    * **Batch Requests**: Reduce API calls

    ## Providers (No API Key Required)

    * **YFinance**: Equities, ETFs, Crypto, Forex
    * **Federal Reserve**: Interest rates, economic data
    * **SEC**: Company filings, insider trading
    * **CBOE**: Options chains
    * **ECB**: European exchange rates
    * **CFTC**: Commitment of Traders reports

    ## Rate Limits

    * No authentication required
    * No rate limiting (open API)
    * Please use responsibly
    """,
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# ============================================================================
# Middleware
# ============================================================================

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)

# GZip compression for responses > 1KB
app.add_middleware(GZipMiddleware, minimum_size=settings.GZIP_MIN_SIZE)

# Cache middleware (optional, can be disabled via settings)
if settings.CACHE_ENABLED:
    app.add_middleware(CacheMiddleware, cache_get_requests=True)


# ============================================================================
# Exception Handlers
# ============================================================================

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler."""
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "An unexpected error occurred",
                "detail": str(exc) if settings.APP_VERSION.startswith("dev") else None
            }
        }
    )


# ============================================================================
# Health Check
# ============================================================================

@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": settings.APP_VERSION,
        "timestamp": datetime.now().isoformat(),
        "cache_enabled": settings.CACHE_ENABLED
    }


# ============================================================================
# Root Endpoint
# ============================================================================

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information."""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "description": "Mobile-optimized financial data API using OpenBB Platform",
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/health",
        "endpoints": {
            "equity": f"{settings.API_PREFIX}/yfinance/quote",
            "crypto": f"{settings.API_PREFIX}/yfinance/crypto/quote",
            "economy": f"{settings.API_PREFIX}/fed/treasury/rates",
            "sec": f"{settings.API_PREFIX}/sec/filings"
        }
    }


# ============================================================================
# Include Routers
# ============================================================================

app.include_router(
    equity_router,
    prefix=settings.API_PREFIX,
    tags=["Equity"]
)

app.include_router(
    economy_router,
    prefix=settings.API_PREFIX,
    tags=["Economy"]
)

app.include_router(
    regulators_router,
    prefix=settings.API_PREFIX,
    tags=["Regulators"]
)

app.include_router(
    crypto_router,
    prefix=settings.API_PREFIX,
    tags=["Crypto"]
)

app.include_router(
    currency_router,
    prefix=settings.API_PREFIX,
    tags=["Currency"]
)

app.include_router(
    etf_router,
    prefix=settings.API_PREFIX,
    tags=["ETF"]
)

app.include_router(
    extra_providers_router,
    prefix=settings.API_PREFIX,
    tags=["Extra Providers"]
)


# ============================================================================
# Main Entry Point
# ============================================================================

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Enable auto-reload for development
        log_level="info"
    )
