"""
ETF router - YFinance ETF endpoints.

Handles ETF-related endpoints using yfinance provider.
"""
from fastapi import APIRouter, Query, HTTPException, Depends

from app.models.responses import ETFInfoResponse
from app.services.openbb_service import get_openbb_service, OpenBBService
from app.services.data_transformer import get_data_transformer, DataTransformer

router = APIRouter()


@router.get("/yfinance/etf/info", response_model=ETFInfoResponse)
async def get_etf_info(
    symbol: str = Query(..., description="ETF symbol (e.g., SPY, QQQ)"),
    fields: str = Query(None, description="Comma-separated fields to return"),
    obb: OpenBBService = Depends(get_openbb_service),
    transformer: DataTransformer = Depends(get_data_transformer)
):
    """
    Get ETF information.

    Returns details about the ETF including expense ratio and holdings.
    """
    try:
        data = await obb.get_etf_info(symbol)
        if not data:
            raise HTTPException(status_code=404, detail=f"ETF info not found for {symbol}")

        # Transform to ETF response format
        response = {
            "symbol": data.get("symbol", symbol),
            "name": data.get("name"),
            "expense_ratio": data.get("expense_ratio"),  # Would need to be extracted
            "assets_under_management": data.get("market_cap"),
            "nav_price": data.get("price"),
            "description": data.get("description")
        }

        if fields:
            response = transformer.filter_fields(response, fields)

        return transformer.sanitize_for_mobile(response)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/yfinance/etf/historical")
async def get_etf_historical(
    symbol: str = Query(..., description="ETF symbol"),
    start_date: str = Query(..., description="Start date (YYYY-MM-DD)"),
    end_date: str = Query(..., description="End date (YYYY-MM-DD)"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(50, ge=1, le=200, description="Items per page"),
    obb: OpenBBService = Depends(get_openbb_service),
    transformer: DataTransformer = Depends(get_data_transformer)
):
    """
    Get ETF historical prices.

    Returns OHLCV data with pagination.
    """
    try:
        data = await obb.get_etf_historical(symbol, start_date, end_date)
        paginated_data, pagination = transformer.paginate_data(data, page, limit)

        return {
            "data": paginated_data,
            "pagination": pagination
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
