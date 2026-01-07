"""
Economy router - Federal Reserve and FRED endpoints.

Handles economy-related endpoints using federal_reserve provider.
"""
from fastapi import APIRouter, Query, HTTPException, Depends
from typing import List

from app.models.responses import (
    TreasuryRateResponse,
    FederalFundsRateResponse,
    SOFRRateResponse,
    YieldCurveResponse
)
from app.services.openbb_service import get_openbb_service, OpenBBService
from app.services.data_transformer import get_data_transformer, DataTransformer

router = APIRouter()


# =============================================================================
# Federal Reserve Endpoints
# =============================================================================

@router.get("/fed/treasury/rates")
async def get_treasury_rates(
    obb: OpenBBService = Depends(get_openbb_service),
    transformer: DataTransformer = Depends(get_data_transformer)
):
    """
    Get Treasury yield curve rates.

    Returns rates for various maturities (1M, 3M, 6M, 1Y, 2Y, 5Y, 10Y, 30Y).
    """
    try:
        data = await obb.get_treasury_rates()
        return [transformer.sanitize_for_mobile(item) for item in data]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/fed/federal/funds/rate", response_model=FederalFundsRateResponse)
async def get_federal_funds_rate(
    obb: OpenBBService = Depends(get_openbb_service),
    transformer: DataTransformer = Depends(get_data_transformer)
):
    """
    Get current federal funds rate.

    Returns the current FFR with target range if available.
    """
    try:
        data = await obb.get_federal_funds_rate()
        if not data:
            raise HTTPException(status_code=404, detail="Federal funds rate not found")

        return transformer.sanitize_for_mobile(data)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/fed/sofr/rate", response_model=SOFRRateResponse)
async def get_sofr_rate(
    obb: OpenBBService = Depends(get_openbb_service),
    transformer: DataTransformer = Depends(get_data_transformer)
):
    """
    Get current SOFR (Secured Overnight Financing Rate).

    SOFR is a key interest rate benchmark.
    """
    try:
        data = await obb.get_sofr_rate()
        if not data:
            raise HTTPException(status_code=404, detail="SOFR rate not found")

        return transformer.sanitize_for_mobile(data)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/fed/yield/curve")
async def get_yield_curve(
    obb: OpenBBService = Depends(get_openbb_service),
    transformer: DataTransformer = Depends(get_data_transformer)
):
    """
    Get yield curve data.

    Returns historical yield curve data across multiple maturities.
    """
    try:
        data = await obb.get_yield_curve()
        return [transformer.sanitize_for_mobile(item) for item in data]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
