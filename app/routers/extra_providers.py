"""
Derivatives and European Economy Router - CBOE, ECB, and CFTC endpoints.
"""
from fastapi import APIRouter, Query, HTTPException, Depends
from typing import List

from app.models.responses import (
    OptionsChainResponse,
    COTReportResponse
)
from app.services.openbb_service import get_openbb_service, OpenBBService
from app.services.data_transformer import get_data_transformer, DataTransformer

router = APIRouter()

@router.get("/cboe/options/chains")
async def get_options_chains(
    symbol: str = Query(..., description="Stock symbol (e.g., AAPL)"),
    obb: OpenBBService = Depends(get_openbb_service),
    transformer: DataTransformer = Depends(get_data_transformer)
):
    """Get options chain data from CBOE."""
    try:
        data = await obb.get_options_chains(symbol)
        return [transformer.sanitize_for_mobile(item) for item in data]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/ecb/forex")
async def get_ecb_forex(
    symbol: str = Query("EURUSD", description="Currency pair"),
    obb: OpenBBService = Depends(get_openbb_service),
    transformer: DataTransformer = Depends(get_data_transformer)
):
    """Get exchange rates from ECB."""
    try:
        data = await obb.get_ecb_forex(symbol)
        return [transformer.sanitize_for_mobile(item) for item in data]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/cftc/cot")
async def get_cot_report(
    symbol: str = Query(..., description="Market ID or Commodity name"),
    obb: OpenBBService = Depends(get_openbb_service),
    transformer: DataTransformer = Depends(get_data_transformer)
):
    """Get Commitment of Traders (COT) report from CFTC."""
    try:
        data = await obb.get_cot_report(symbol)
        return [transformer.sanitize_for_mobile(item) for item in data]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
