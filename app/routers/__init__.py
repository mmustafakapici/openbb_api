"""Routers package."""

from .equity import router as equity_router
from .economy import router as economy_router
from .regulators import router as regulators_router
from .crypto import router as crypto_router
from .currency import router as currency_router
from .etf import router as etf_router
from .extra_providers import router as extra_providers_router

from .extra_providers import router as extra_providers_router

__all__ = [
    "equity_router",
    "economy_router",
    "regulators_router",
    "crypto_router",
    "currency_router",
    "etf_router",
    "extra_providers_router",
]
