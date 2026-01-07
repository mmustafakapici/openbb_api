"""
Currency router - YFinance forex endpoints.

Handles currency/forex-related endpoints using yfinance provider.
"""
from fastapi import APIRouter, Query, HTTPException, Depends

from app.models.responses import CurrencyQuoteResponse
from app.services.openbb_service import get_openbb_service, OpenBBService
from app.services.data_transformer import get_data_transformer, DataTransformer

router = APIRouter()


@router.get("/yfinance/currency/quote", response_model=CurrencyQuoteResponse)
async def get_currency_quote(
    pair: str = Query("EURUSD=X", description="Currency pair (e.g., EURUSD=X)"),
    fields: str = Query(None, description="Comma-separated fields to return"),
    obb: OpenBBService = Depends(get_openbb_service),
    transformer: DataTransformer = Depends(get_data_transformer)
):
    """
    Get forex currency pair quote.

    Supports major currency pairs from Yahoo Finance.
    Common pairs: EURUSD=X, GBPUSD=X, USDJPY=X, USDTRY=X
    """
    try:
        data = await obb.get_equity_quote(pair)
        if not data or data.get("price", 0) == 0:
            raise HTTPException(status_code=404, detail=f"Currency quote not found for {pair}")

        # Transform to currency response format
        response = {
            "pair": pair,
            "rate": data.get("price", 0),
            "change": data.get("change", 0),
            "change_percent": data.get("change_percent", 0),
            "last_updated": data.get("last_updated")
        }

        if fields:
            response = transformer.filter_fields(response, fields)

        return transformer.sanitize_for_mobile(response)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/yfinance/currency/historical")
async def get_currency_historical(
    pair: str = Query("EURUSD=X", description="Currency pair"),
    start_date: str = Query(..., description="Start date (YYYY-MM-DD)"),
    end_date: str = Query(..., description="End date (YYYY-MM-DD)"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(50, ge=1, le=200, description="Items per page"),
    obb: OpenBBService = Depends(get_openbb_service),
    transformer: DataTransformer = Depends(get_data_transformer)
):
    """
    Get forex historical rates.

    Returns OHLCV data with pagination.
    """
    try:
        data = await obb.get_currency_historical(pair, start_date, end_date)
        paginated_data, pagination = transformer.paginate_data(data, page, limit)

        return {
            "data": paginated_data,
            "pagination": pagination
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
