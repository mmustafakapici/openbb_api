"""
Request models for API endpoints.
"""
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional, List


# =============================================================================
# Query Parameters
# =============================================================================

class SymbolQuery(BaseModel):
    """Symbol query parameter."""

    symbol: str = Field(..., description="Stock/crypto symbol (e.g., AAPL, BTC-USD)")


class DateRangeQuery(BaseModel):
    """Date range query parameters."""

    start_date: str = Field(..., description="Start date (YYYY-MM-DD)")
    end_date: str = Field(..., description="End date (YYYY-MM-DD)")

    @field_validator("start_date", "end_date")
    @classmethod
    def validate_date(cls, v: str) -> str:
        """Validate date format."""
        try:
            datetime.strptime(v, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Date must be in YYYY-MM-DD format")
        return v


class PaginationQuery(BaseModel):
    """Pagination query parameters."""

    page: int = Field(1, ge=1, description="Page number")
    limit: int = Field(50, ge=1, le=200, description="Items per page")


class FieldFilterQuery(BaseModel):
    """Field filtering query parameter."""

    fields: Optional[str] = Field(None, description="Comma-separated fields to return")


# =============================================================================
# Request Bodies
# =============================================================================

class BatchQuotesRequest(BaseModel):
    """Batch quotes request body."""

    symbols: List[str] = Field(..., min_length=1, max_length=100, description="List of symbols")
    fields: Optional[str] = Field(None, description="Comma-separated fields to return")


class SymbolsListRequest(BaseModel):
    """List of symbols request."""

    symbols: List[str] = Field(..., min_length=1, max_length=100)
