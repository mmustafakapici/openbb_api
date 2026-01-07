"""
Crypto router - YFinance crypto endpoints.

Handles cryptocurrency-related endpoints using yfinance provider.
"""
from fastapi import APIRouter, Query, HTTPException, Depends

from app.models.responses import CryptoQuoteResponse
from app.services.openbb_service import get_openbb_service, OpenBBService
from app.services.data_transformer import get_data_transformer, DataTransformer

router = APIRouter()


@router.get("/yfinance/crypto/quote", response_model=CryptoQuoteResponse)
async def get_crypto_quote(
    symbol: str = Query("BTC-USD", description="Crypto symbol (e.g., BTC-USD, ETH-USD)"),
    fields: str = Query(None, description="Comma-separated fields to return"),
    obb: OpenBBService = Depends(get_openbb_service),
    transformer: DataTransformer = Depends(get_data_transformer)
):
    """
    Get cryptocurrency quote.

    Supports major cryptocurrencies from Yahoo Finance.
    Common symbols: BTC-USD, ETH-USD, BNB-USD, XRP-USD, ADA-USD, SOL-USD, DOGE-USD
    """
    try:
        data = await obb.get_crypto_quote(symbol)
        if not data:
            raise HTTPException(status_code=404, detail=f"Crypto quote not found for {symbol}")

        # Map symbol to pair for consistency
        data["pair"] = data.get("symbol", symbol)
        data["name"] = data.get("name", symbol.split("-")[0])

        if fields:
            data = transformer.filter_fields(data, fields)

        return transformer.sanitize_for_mobile(data)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/yfinance/crypto/historical")
async def get_crypto_historical(
    symbol: str = Query("BTC-USD", description="Crypto symbol"),
    start_date: str = Query(..., description="Start date (YYYY-MM-DD)"),
    end_date: str = Query(..., description="End date (YYYY-MM-DD)"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(50, ge=1, le=200, description="Items per page"),
    obb: OpenBBService = Depends(get_openbb_service),
    transformer: DataTransformer = Depends(get_data_transformer)
):
    """
    Get cryptocurrency historical prices.

    Returns OHLCV data with pagination.
    """
    try:
        data = await obb.get_crypto_historical(symbol, start_date, end_date)
        paginated_data, pagination = transformer.paginate_data(data, page, limit)

        return {
            "data": paginated_data,
            "pagination": pagination
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
