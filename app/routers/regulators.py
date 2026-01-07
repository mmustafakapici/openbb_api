"""
Regulators router - SEC and other regulatory endpoints.

Handles regulatory data endpoints using SEC provider.
"""
from fastapi import APIRouter, Query, HTTPException, Depends
from typing import Optional

from app.models.responses import (
    SECFilingResponse,
    InsiderTradeResponse
)
from app.services.openbb_service import get_openbb_service, OpenBBService
from app.services.data_transformer import get_data_transformer, DataTransformer

router = APIRouter()


# =============================================================================
# SEC Endpoints
# =============================================================================

@router.get("/sec/filings")
async def get_sec_filings(
    symbol: str = Query(..., description="Stock symbol"),
    filing_type: Optional[str] = Query(None, description="Filter by filing type (e.g., 10-K, 10-Q)"),
    limit: int = Query(20, ge=1, le=100, description="Number of results"),
    obb: OpenBBService = Depends(get_openbb_service),
    transformer: DataTransformer = Depends(get_data_transformer)
):
    """
    Get SEC filings for a company.

    Returns recent SEC filings including 10-K, 10-Q, 8-K, etc.
    """
    try:
        data = await obb.get_sec_filings(symbol, filing_type, limit)
        return [transformer.sanitize_for_mobile(item) for item in data]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sec/insider/trading")
async def get_insider_trading(
    symbol: str = Query(..., description="Stock symbol"),
    limit: int = Query(20, ge=1, le=100, description="Number of results"),
    obb: OpenBBService = Depends(get_openbb_service),
    transformer: DataTransformer = Depends(get_data_transformer)
):
    """
    Get insider trading data for a company.

    Returns recent insider buys/sells by company executives.
    """
    try:
        data = await obb.get_insider_trading(symbol, limit)
        return [transformer.sanitize_for_mobile(item) for item in data]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
