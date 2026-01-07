"""
Error models for API responses.
"""
from pydantic import BaseModel
from typing import Optional, Dict, Any


class ErrorDetail(BaseModel):
    """Error detail model."""

    code: str
    message: str
    details: Optional[Dict[str, Any]] = None


class ErrorResponse(BaseModel):
    """Standard error response."""

    success: bool = False
    error: ErrorDetail


# Common error codes
class ErrorCode:
    """Error code constants."""

    INVALID_SYMBOL = "INVALID_SYMBOL"
    INVALID_DATE_RANGE = "INVALID_DATE_RANGE"
    PROVIDER_ERROR = "PROVIDER_ERROR"
    NOT_FOUND = "NOT_FOUND"
    RATE_LIMITED = "RATE_LIMITED"
    INTERNAL_ERROR = "INTERNAL_ERROR"
    VALIDATION_ERROR = "VALIDATION_ERROR"
