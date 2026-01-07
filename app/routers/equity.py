"""
Equity router - YFinance provider endpoints.

Handles all equity-related endpoints using yfinance provider.
"""
from fastapi import APIRouter, Query, HTTPException, Depends
from typing import Optional, List

from app.models.responses import (
    EquityQuoteResponse,
    EquityHistoricalData,
    EquityProfileResponse,
    ScreenerItem,
    BatchQuotesResponse,
    PaginatedResponse
)
from app.models.requests import BatchQuotesRequest
from app.services.openbb_service import get_openbb_service, OpenBBService
from app.services.data_transformer import get_data_transformer, DataTransformer

router = APIRouter()


# =============================================================================
# Quote Endpoints
# =============================================================================

@router.get("/yfinance/quote", response_model=EquityQuoteResponse)
async def get_equity_quote(
    symbol: str = Query(..., description="Stock symbol (e.g., AAPL)"),
    fields: Optional[str] = Query(None, description="Comma-separated fields to return"),
    obb: OpenBBService = Depends(get_openbb_service),
    transformer: DataTransformer = Depends(get_data_transformer)
):
    """
    Get real-time stock quote.

    Returns current stock price with essential mobile-optimized fields.
    """
    try:
        data = await obb.get_equity_quote(symbol)
        if not data:
            raise HTTPException(status_code=404, detail=f"Quote not found for {symbol}")

        # Filter fields if requested
        if fields:
            data = transformer.filter_fields(data, fields)

        # Sanitize for mobile
        data = transformer.sanitize_for_mobile(data)
        return data

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/yfinance/batch/quotes", response_model=BatchQuotesResponse)
async def get_batch_quotes(
    request: BatchQuotesRequest,
    obb: OpenBBService = Depends(get_openbb_service),
    transformer: DataTransformer = Depends(get_data_transformer)
):
    """
    Get quotes for multiple symbols in one request.

    Reduces API calls for mobile apps fetching multiple stocks.
    """
    from datetime import datetime

    results = {}
    success_count = 0
    error_count = 0

    for symbol in request.symbols:
        try:
            data = await obb.get_equity_quote(symbol)
            if data:
                if request.fields:
                    data = transformer.filter_fields(data, request.fields)
                data = transformer.sanitize_for_mobile(data)
                results[symbol] = data
                success_count += 1
            else:
                results[symbol] = {"error": "Not found"}
                error_count += 1
        except Exception as e:
            results[symbol] = {"error": str(e)}
            error_count += 1

    return {
        "data": results,
        "success_count": success_count,
        "error_count": error_count,
        "timestamp": datetime.now()
    }


# =============================================================================
# Historical Data Endpoints
# =============================================================================

@router.get("/yfinance/historical")
async def get_equity_historical(
    symbol: str = Query(..., description="Stock symbol"),
    start_date: str = Query(..., description="Start date (YYYY-MM-DD)"),
    end_date: str = Query(..., description="End date (YYYY-MM-DD)"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(50, ge=1, le=200, description="Items per page"),
    obb: OpenBBService = Depends(get_openbb_service),
    transformer: DataTransformer = Depends(get_data_transformer)
):
    """
    Get historical price data with pagination.

    Returns OHLCV data with mobile-optimized pagination.
    """
    try:
        data = await obb.get_equity_historical(symbol, start_date, end_date)

        # Paginate
        paginated_data, pagination = transformer.paginate_data(data, page, limit)

        # Sanitize dates
        for item in paginated_data:
            if "date" in item and isinstance(item["date"], str):
                item["date"] = item["date"]  # Already ISO format from service

        return {
            "data": paginated_data,
            "pagination": pagination
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =============================================================================
# Profile Endpoints
# =============================================================================

@router.get("/yfinance/profile", response_model=EquityProfileResponse)
async def get_equity_profile(
    symbol: str = Query(..., description="Stock symbol"),
    fields: Optional[str] = Query(None, description="Comma-separated fields to return"),
    obb: OpenBBService = Depends(get_openbb_service),
    transformer: DataTransformer = Depends(get_data_transformer)
):
    """Get company profile information."""
    try:
        data = await obb.get_equity_profile(symbol)
        if not data:
            raise HTTPException(status_code=404, detail=f"Profile not found for {symbol}")

        if fields:
            data = transformer.filter_fields(data, fields)

        return transformer.sanitize_for_mobile(data)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =============================================================================
# Screener Endpoints
# =============================================================================

@router.get("/yfinance/screener/gainers")
async def get_screener_gainers(
    limit: int = Query(20, ge=1, le=100, description="Number of results"),
    obb: OpenBBService = Depends(get_openbb_service),
    transformer: DataTransformer = Depends(get_data_transformer)
):
    """Get top gaining stocks."""
    try:
        data = await obb.get_screener_gainers(limit)
        return [transformer.sanitize_for_mobile(item) for item in data]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/yfinance/screener/losers")
async def get_screener_losers(
    limit: int = Query(20, ge=1, le=100, description="Number of results"),
    obb: OpenBBService = Depends(get_openbb_service),
    transformer: DataTransformer = Depends(get_data_transformer)
):
    """Get top losing stocks."""
    try:
        data = await obb.get_screener_losers(limit)
        return [transformer.sanitize_for_mobile(item) for item in data]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/yfinance/screener/active")
async def get_screener_active(
    limit: int = Query(20, ge=1, le=100, description="Number of results"),
    obb: OpenBBService = Depends(get_openbb_service),
    transformer: DataTransformer = Depends(get_data_transformer)
):
    """Get most active stocks by volume."""
    try:
        data = await obb.get_screener_active(limit)
        return [transformer.sanitize_for_mobile(item) for item in data]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
