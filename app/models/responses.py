"""
Mobile-optimized Pydantic response models.

These models transform OpenBB's verbose responses (50+ fields)
into lightweight mobile responses (5-10 fields).
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List, Any, Dict


# =============================================================================
# Base Response Models
# =============================================================================

class APIResponse(BaseModel):
    """Standard API response wrapper."""

    success: bool = True
    message: Optional[str] = None
    data: Optional[Any] = None


class PaginationMeta(BaseModel):
    """Pagination metadata."""

    page: int
    limit: int
    total: int
    total_pages: int
    has_next: bool
    has_prev: bool


class PaginatedResponse(BaseModel):
    """Paginated response wrapper."""

    data: List[Any]
    pagination: PaginationMeta


# =============================================================================
# Error Models
# =============================================================================

class ErrorResponse(BaseModel):
    """Error response model."""

    success: bool = False
    error: str
    detail: Optional[str] = None
    code: Optional[str] = None


# =============================================================================
# YFinance - Equity Models
# =============================================================================

class EquityQuoteResponse(BaseModel):
    """Mobile-optimized equity quote response."""

    symbol: str
    name: Optional[str] = None
    price: float
    change: float
    change_percent: float
    volume: Optional[int] = None
    market_cap: Optional[int] = None
    last_updated: datetime

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class EquityHistoricalData(BaseModel):
    """Historical price data point."""

    date: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int


class EquityProfileResponse(BaseModel):
    """Company profile response."""

    symbol: str
    name: Optional[str] = None
    sector: Optional[str] = None
    industry: Optional[str] = None
    market_cap: Optional[int] = None
    website: Optional[str] = None
    description: Optional[str] = None
    country: Optional[str] = None
    currency: Optional[str] = None


class ScreenerItem(BaseModel):
    """Screener result item."""

    symbol: str
    name: Optional[str] = None
    price: float
    change: float
    change_percent: float
    volume: Optional[int] = None


# =============================================================================
# YFinance - ETF Models
# =============================================================================

class ETFInfoResponse(BaseModel):
    """ETF information response."""

    symbol: str
    name: Optional[str] = None
    expense_ratio: Optional[float] = None
    assets_under_management: Optional[float] = None
    nav_price: Optional[float] = None
    description: Optional[str] = None


# =============================================================================
# YFinance - Crypto Models
# =============================================================================

class CryptoQuoteResponse(BaseModel):
    """Crypto quote response."""

    symbol: str
    name: Optional[str] = None
    price: float
    change_24h: float
    change_percent_24h: float
    volume_24h: Optional[float] = None
    market_cap: Optional[float] = None
    last_updated: datetime


# =============================================================================
# YFinance - Currency Models
# =============================================================================

class CurrencyQuoteResponse(BaseModel):
    """Currency quote response."""

    pair: str
    rate: float
    change: float
    change_percent: float
    last_updated: datetime


# =============================================================================
# Federal Reserve Models
# =============================================================================

class TreasuryRateResponse(BaseModel):
    """Treasury rate response."""

    maturity: str
    rate: float
    date: datetime


class FederalFundsRateResponse(BaseModel):
    """Federal funds rate response."""

    rate: float
    date: datetime
    target_range_lower: Optional[float] = None
    target_range_upper: Optional[float] = None


class SOFRRateResponse(BaseModel):
    """SOFR rate response."""

    rate: float
    date: datetime


class YieldCurveResponse(BaseModel):
    """Yield curve data point."""

    date: datetime
    rate_1m: Optional[float] = None
    rate_3m: Optional[float] = None
    rate_6m: Optional[float] = None
    rate_1y: Optional[float] = None
    rate_2y: Optional[float] = None
    rate_5y: Optional[float] = None
    rate_10y: Optional[float] = None
    rate_30y: Optional[float] = None


# =============================================================================
# SEC Models
# =============================================================================

class SECFilingResponse(BaseModel):
    """SEC filing response."""

    symbol: str
    filing_type: str
    filing_date: datetime
    filed_date: Optional[datetime] = None
    url: Optional[str] = None
    description: Optional[str] = None


class InsiderTradeResponse(BaseModel):
    """Insider trading response."""

    symbol: str
    insider_name: Optional[str] = None
    transaction_type: Optional[str] = None
    shares: Optional[float] = None
    price: Optional[float] = None
    transaction_date: Optional[datetime] = None


# =============================================================================
# FRED Models (Optional API Key)
# =============================================================================

class FREDSeriesResponse(BaseModel):
    """FRED series data point."""

    date: datetime
    value: float


class FREDInfoResponse(BaseModel):
    """FRED series info."""

    series_id: str
    title: Optional[str] = None
    units: Optional[str] = None
    frequency: Optional[str] = None
    last_updated: Optional[datetime] = None


# =============================================================================
# Batch Response Models
# =============================================================================

class BatchQuotesResponse(BaseModel):
    """Batch quotes response."""

    data: Dict[str, EquityQuoteResponse]
    success_count: int
    error_count: int
    timestamp: datetime


# =============================================================================
# Health Check
# =============================================================================

# =============================================================================
# New Providers - CBOE, ECB, CFTC
# =============================================================================

class OptionsChainResponse(BaseModel):
    """Mobile-optimized options chain response."""
    
    expiration: str
    strike: float
    option_type: str
    last_price: Optional[float] = None
    bid: Optional[float] = None
    ask: Optional[float] = None
    volume: Optional[int] = None
    open_interest: Optional[int] = None
    implied_volatility: Optional[float] = None

class COTReportResponse(BaseModel):
    """Commitment of Traders (COT) report data."""
    
    date: datetime
    market: str
    non_commercial_long: Optional[int] = None
    non_commercial_short: Optional[int] = None
    commercial_long: Optional[int] = None
    commercial_short: Optional[int] = None
    open_interest: Optional[int] = None

class HealthResponse(BaseModel):
    """Health check response."""

    status: str
    version: str
    timestamp: datetime
    cache_enabled: bool
