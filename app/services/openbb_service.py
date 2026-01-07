"""
OpenBB Platform API wrapper service.

This service wraps the OpenBB Python SDK to fetch data from free providers.
"""
import asyncio
from datetime import datetime
from typing import Optional, List, Any, Dict
import pandas as pd

from app.config import settings


class OpenBBService:
    """
    Wrapper service for OpenBB Platform API.

    Handles all interactions with the OpenBB SDK and transforms
    responses into mobile-optimized formats.
    """

    def __init__(self):
        """Initialize OpenBB service."""
        self._obb = None
        self._initialize_openbb()

    def _initialize_openbb(self):
        """Initialize OpenBB SDK."""
        try:
            from openbb import obb
            self._obb = obb
        except ImportError as e:
            raise RuntimeError(
                f"OpenBB package not found. Make sure it's installed: {e}"
            )

    # ========================================================================
    # YFinance - Equity Methods
    # ========================================================================

    async def get_equity_quote(
        self,
        symbol: str,
        provider: str = "yfinance"
    ) -> Dict[str, Any]:
        """
        Get real-time equity quote.

        Args:
            symbol: Stock symbol (e.g., AAPL)
            provider: Data provider (default: yfinance)

        Returns:
            Dict with quote data
        """
        try:
            result = self._obb.equity.price.quote(
                symbol=symbol,
                provider=provider
            )
            return self._extract_quote_data(result, symbol)
        except Exception as e:
            raise RuntimeError(f"Error fetching quote for {symbol}: {e}")

    async def get_equity_historical(
        self,
        symbol: str,
        start_date: str,
        end_date: str,
        provider: str = "yfinance"
    ) -> List[Dict[str, Any]]:
        """
        Get historical equity prices.

        Args:
            symbol: Stock symbol
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            provider: Data provider

        Returns:
            List of historical data points
        """
        try:
            result = self._obb.equity.price.historical(
                symbol=symbol,
                start_date=start_date,
                end_date=end_date,
                provider=provider
            )
            return self._extract_historical_data(result)
        except Exception as e:
            raise RuntimeError(f"Error fetching historical data for {symbol}: {e}")

    async def get_equity_profile(
        self,
        symbol: str,
        provider: str = "yfinance"
    ) -> Dict[str, Any]:
        """
        Get company profile.

        Args:
            symbol: Stock symbol
            provider: Data provider

        Returns:
            Dict with profile data
        """
        try:
            result = self._obb.equity.profile(
                symbol=symbol,
                provider=provider
            )
            return self._extract_profile_data(result)
        except Exception as e:
            raise RuntimeError(f"Error fetching profile for {symbol}: {e}")

    async def get_screener_gainers(
        self,
        limit: int = 20,
        provider: str = "yfinance"
    ) -> List[Dict[str, Any]]:
        """Get top gainers from screener."""
        try:
            result = self._obb.equity.discovery.gainers(
                provider=provider
            )
            return self._extract_screener_data(result, limit)
        except Exception as e:
            raise RuntimeError(f"Error fetching gainers: {e}")

    async def get_screener_losers(
        self,
        limit: int = 20,
        provider: str = "yfinance"
    ) -> List[Dict[str, Any]]:
        """Get top losers from screener."""
        try:
            result = self._obb.equity.discovery.losers(
                provider=provider
            )
            return self._extract_screener_data(result, limit)
        except Exception as e:
            raise RuntimeError(f"Error fetching losers: {e}")

    async def get_screener_active(
        self,
        limit: int = 20,
        provider: str = "yfinance"
    ) -> List[Dict[str, Any]]:
        """Get most active stocks."""
        try:
            result = self._obb.equity.discovery.active(
                provider=provider
            )
            return self._extract_screener_data(result, limit)
        except Exception as e:
            raise RuntimeError(f"Error fetching active stocks: {e}")

    # ========================================================================
    # YFinance - ETF Methods
    # ========================================================================

    async def get_etf_historical(
        self,
        symbol: str,
        start_date: str,
        end_date: str,
        provider: str = "yfinance"
    ) -> List[Dict[str, Any]]:
        """Get ETF historical prices."""
        return await self.get_equity_historical(symbol, start_date, end_date, provider)

    async def get_etf_info(
        self,
        symbol: str,
        provider: str = "yfinance"
    ) -> Dict[str, Any]:
        """Get ETF information."""
        return await self.get_equity_profile(symbol, provider)

    # ========================================================================
    # YFinance - Crypto Methods
    # ========================================================================

    async def get_crypto_quote(
        self,
        symbol: str = "BTC-USD",
        provider: str = "yfinance"
    ) -> Dict[str, Any]:
        """Get crypto quote."""
        return await self.get_equity_quote(symbol, provider)

    async def get_crypto_historical(
        self,
        symbol: str,
        start_date: str,
        end_date: str,
        provider: str = "yfinance"
    ) -> List[Dict[str, Any]]:
        """Get crypto historical prices."""
        return await self.get_equity_historical(symbol, start_date, end_date, provider)

    # ========================================================================
    # YFinance - Currency Methods
    # ========================================================================

    async def get_currency_historical(
        self,
        symbol: str,
        start_date: str,
        end_date: str,
        provider: str = "yfinance"
    ) -> List[Dict[str, Any]]:
        """Get currency historical rates."""
        return await self.get_equity_historical(symbol, start_date, end_date, provider)

    # ========================================================================
    # Federal Reserve Methods
    # ========================================================================

    async def get_treasury_rates(
        self,
        provider: str = "federal_reserve"
    ) -> List[Dict[str, Any]]:
        """Get Treasury yield curve rates."""
        try:
            result = self._obb.economy.treasury_rates(
                provider=provider
            )
            return self._extract_treasury_rates(result)
        except Exception as e:
            raise RuntimeError(f"Error fetching treasury rates: {e}")

    async def get_federal_funds_rate(
        self,
        provider: str = "federal_reserve"
    ) -> Dict[str, Any]:
        """Get federal funds rate."""
        try:
            result = self._obb.economy.federal_funds_rate(
                provider=provider
            )
            return self._extract_fed_funds_rate(result)
        except Exception as e:
            raise RuntimeError(f"Error fetching federal funds rate: {e}")

    async def get_sofr_rate(
        self,
        provider: str = "federal_reserve"
    ) -> Dict[str, Any]:
        """Get SOFR rate."""
        try:
            result = self._obb.economy.sofr(
                provider=provider
            )
            return self._extract_sofr_rate(result)
        except Exception as e:
            raise RuntimeError(f"Error fetching SOFR rate: {e}")

    async def get_yield_curve(
        self,
        provider: str = "federal_reserve"
    ) -> List[Dict[str, Any]]:
        """Get yield curve data."""
        try:
            result = self._obb.economy.yield_curve(
                provider=provider
            )
            return self._extract_yield_curve(result)
        except Exception as e:
            raise RuntimeError(f"Error fetching yield curve: {e}")

    # ========================================================================
    # SEC Methods
    # ========================================================================

    async def get_sec_filings(
        self,
        symbol: str,
        filing_type: Optional[str] = None,
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """Get SEC filings for a symbol."""
        try:
            result = self._obb.equity.filings(
                symbol=symbol,
                filing_type=filing_type,
                limit=limit,
                provider="sec"
            )
            return self._extract_sec_filings(result, symbol)
        except Exception as e:
            raise RuntimeError(f"Error fetching SEC filings: {e}")

    async def get_insider_trading(
        self,
        symbol: str,
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """Get insider trading data."""
        try:
            result = self._obb.regulators.insider_trading(
                symbol=symbol,
                limit=limit,
                provider="sec"
            )
            return self._extract_insider_trading(result, symbol)
        except Exception as e:
            raise RuntimeError(f"Error fetching insider trading: {e}")

    # ========================================================================
    # CBOE Methods
    # ========================================================================

    async def get_options_chains(
        self,
        symbol: str,
        provider: str = "cboe"
    ) -> List[Dict[str, Any]]:
        """Get options chain data."""
        try:
            result = self._obb.derivatives.options.chains(
                symbol=symbol,
                provider=provider
            )
            return self._extract_options_data(result)
        except Exception as e:
            raise RuntimeError(f"Error fetching options for {symbol}: {e}")

    # ========================================================================
    # ECB Methods
    # ========================================================================

    async def get_ecb_forex(
        self,
        symbol: str = "EURUSD",
        provider: str = "ecb"
    ) -> List[Dict[str, Any]]:
        """Get ECB exchange rates."""
        try:
            # Note: OpenBB usually maps ECB to fixedincome/rate or similar
            result = self._obb.fixedincome.rate.ecb(
                provider=provider
            )
            return self._extract_ecb_data(result)
        except Exception as e:
            raise RuntimeError(f"Error fetching ECB rates: {e}")

    # ========================================================================
    # CFTC Methods
    # ========================================================================

    async def get_cot_report(
        self,
        symbol: str,
        provider: str = "cftc"
    ) -> List[Dict[str, Any]]:
        """Get Commitment of Traders (COT) report."""
        try:
            result = self._obb.regulators.cftc.cot(
                id=symbol,
                provider=provider
            )
            return self._extract_cot_data(result)
        except Exception as e:
            raise RuntimeError(f"Error fetching COT report for {symbol}: {e}")

    # ========================================================================
    # Data Extraction Helpers
    # ========================================================================

    def _extract_quote_data(self, result, symbol: str) -> Dict[str, Any]:
        """Extract quote data from OpenBB result."""
        try:
            df = result.to_df() if hasattr(result, 'to_df') else result
            if df is None or df.empty:
                return {}

            row = df.iloc[0] if isinstance(df, pd.DataFrame) else df

            return {
                "symbol": symbol,
                "name": row.get("name", row.get("longName", None)),
                "price": float(row.get("price", row.get("regularMarketPrice", 0))),
                "change": float(row.get("change", row.get("regularMarketChange", 0))),
                "change_percent": float(row.get("change_percent", row.get("regularMarketChangePercent", 0))),
                "volume": int(row.get("volume", row.get("regularMarketVolume", 0))) if row.get("volume") else None,
                "market_cap": int(row.get("market_cap", row.get("marketCap", 0))) if row.get("market_cap") else None,
                "last_updated": datetime.now()
            }
        except Exception:
            return {
                "symbol": symbol,
                "price": 0,
                "change": 0,
                "change_percent": 0,
                "last_updated": datetime.now()
            }

    def _extract_historical_data(self, result) -> List[Dict[str, Any]]:
        """Extract historical data from OpenBB result."""
        try:
            df = result.to_df() if hasattr(result, 'to_df') else result
            if df is None or df.empty:
                return []

            data = []
            for _, row in df.iterrows():
                data.append({
                    "date": row.name if isinstance(row.name, datetime) else datetime.now(),
                    "open": float(row.get("open", 0)),
                    "high": float(row.get("high", 0)),
                    "low": float(row.get("low", 0)),
                    "close": float(row.get("close", 0)),
                    "volume": int(row.get("volume", 0))
                })
            return data
        except Exception:
            return []

    def _extract_profile_data(self, result) -> Dict[str, Any]:
        """Extract profile data from OpenBB result."""
        try:
            df = result.to_df() if hasattr(result, 'to_df') else result
            if df is None or df.empty:
                return {}

            row = df.iloc[0] if isinstance(df, pd.DataFrame) else df
            return {
                "symbol": row.get("symbol", ""),
                "name": row.get("longName", row.get("shortName", None)),
                "sector": row.get("sector", None),
                "industry": row.get("industry", None),
                "market_cap": int(row.get("marketCap", 0)) if row.get("marketCap") else None,
                "website": row.get("website", None),
                "description": row.get("longBusinessSummary", None),
                "country": row.get("country", None),
                "currency": row.get("currency", None)
            }
        except Exception:
            return {}

    def _extract_screener_data(self, result, limit: int) -> List[Dict[str, Any]]:
        """Extract screener data from OpenBB result."""
        try:
            df = result.to_df() if hasattr(result, 'to_df') else result
            if df is None or df.empty:
                return []

            data = []
            for _, row in df.head(limit).iterrows():
                data.append({
                    "symbol": row.get("symbol", ""),
                    "name": row.get("name", row.get("longName", None)),
                    "price": float(row.get("price", row.get("regularMarketPrice", 0))),
                    "change": float(row.get("change", row.get("regularMarketChange", 0))),
                    "change_percent": float(row.get("change_percent", row.get("regularMarketChangePercent", 0))),
                    "volume": int(row.get("volume", row.get("regularMarketVolume", 0))) if row.get("volume") else None
                })
            return data
        except Exception:
            return []

    def _extract_treasury_rates(self, result) -> List[Dict[str, Any]]:
        """Extract treasury rates from OpenBB result."""
        try:
            df = result.to_df() if hasattr(result, 'to_df') else result
            if df is None or df.empty:
                return []

            data = []
            for _, row in df.iterrows():
                data.append({
                    "date": row.name if isinstance(row.name, datetime) else datetime.now(),
                    "maturity": row.get("maturity", ""),
                    "rate": float(row.get("rate", 0))
                })
            return data
        except Exception:
            return []

    def _extract_fed_funds_rate(self, result) -> Dict[str, Any]:
        """Extract federal funds rate from OpenBB result."""
        try:
            df = result.to_df() if hasattr(result, 'to_df') else result
            if df is None or df.empty:
                return {}

            row = df.iloc[-1] if isinstance(df, pd.DataFrame) else result
            return {
                "rate": float(row.get("rate", 0)),
                "date": row.get("date", datetime.now()),
                "target_range_lower": float(row.get("target_range_lower", 0)) if row.get("target_range_lower") else None,
                "target_range_upper": float(row.get("target_range_upper", 0)) if row.get("target_range_upper") else None
            }
        except Exception:
            return {}

    def _extract_sofr_rate(self, result) -> Dict[str, Any]:
        """Extract SOFR rate from OpenBB result."""
        try:
            df = result.to_df() if hasattr(result, 'to_df') else result
            if df is None or df.empty:
                return {}

            row = df.iloc[-1] if isinstance(df, pd.DataFrame) else result
            return {
                "rate": float(row.get("rate", 0)),
                "date": row.get("date", datetime.now())
            }
        except Exception:
            return {}

    def _extract_yield_curve(self, result) -> List[Dict[str, Any]]:
        """Extract yield curve from OpenBB result."""
        try:
            df = result.to_df() if hasattr(result, 'to_df') else result
            if df is None or df.empty:
                return []

            data = []
            for _, row in df.iterrows():
                data.append({
                    "date": row.get("date", datetime.now()),
                    "rate_1m": float(row["1m"]) if "1m" in row else None,
                    "rate_3m": float(row["3m"]) if "3m" in row else None,
                    "rate_6m": float(row["6m"]) if "6m" in row else None,
                    "rate_1y": float(row["1y"]) if "1y" in row else None,
                    "rate_2y": float(row["2y"]) if "2y" in row else None,
                    "rate_5y": float(row["5y"]) if "5y" in row else None,
                    "rate_10y": float(row["10y"]) if "10y" in row else None,
                    "rate_30y": float(row["30y"]) if "30y" in row else None
                })
            return data
        except Exception:
            return []

    def _extract_sec_filings(self, result, symbol: str) -> List[Dict[str, Any]]:
        """Extract SEC filings from OpenBB result."""
        try:
            df = result.to_df() if hasattr(result, 'to_df') else result
            if df is None or df.empty:
                return []

            data = []
            for _, row in df.iterrows():
                data.append({
                    "symbol": symbol,
                    "filing_type": row.get("filing_type", row.get("form", "")),
                    "filing_date": row.get("filing_date", datetime.now()),
                    "filed_date": row.get("filed_date", None),
                    "url": row.get("url", None),
                    "description": row.get("description", None)
                })
            return data
        except Exception:
            return []

    def _extract_insider_trading(self, result, symbol: str) -> List[Dict[str, Any]]:
        """Extract insider trading data from OpenBB result."""
        try:
            df = result.to_df() if hasattr(result, 'to_df') else result
            if df is None or df.empty:
                return []

            data = []
            for _, row in df.iterrows():
                data.append({
                    "symbol": symbol,
                    "insider_name": row.get("insider_name", None),
                    "transaction_type": row.get("transaction_type", None),
                    "shares": float(row.get("shares", 0)) if row.get("shares") else None,
                    "price": float(row.get("price", 0)) if row.get("price") else None,
                    "transaction_date": row.get("transaction_date", None)
                })
            return data
        except Exception:
            return []

    def _extract_options_data(self, result) -> List[Dict[str, Any]]:
        """Extract options data from OpenBB result."""
        try:
            df = result.to_df() if hasattr(result, 'to_df') else result
            if df is None or df.empty:
                return []

            data = []
            for _, row in df.iterrows():
                data.append({
                    "expiration": str(row.get("expiration")),
                    "strike": float(row.get("strike", 0)),
                    "option_type": row.get("option_type", ""),
                    "last_price": float(row.get("last_price", 0)),
                    "bid": float(row.get("bid", 0)),
                    "ask": float(row.get("ask", 0)),
                    "volume": int(row.get("volume", 0)),
                    "open_interest": int(row.get("open_interest", 0)),
                    "implied_volatility": float(row.get("implied_volatility", 0))
                })
            return data
        except Exception:
            return []

    def _extract_ecb_data(self, result) -> List[Dict[str, Any]]:
        """Extract ECB data from OpenBB result."""
        try:
            df = result.to_df() if hasattr(result, 'to_df') else result
            if df is None or df.empty:
                return []
            
            data = []
            for _, row in df.iterrows():
                data.append({
                    "date": row.name if isinstance(row.name, datetime) else datetime.now(),
                    "rate": float(row.get("rate", 0))
                })
            return data
        except Exception:
            return []

    def _extract_cot_data(self, result) -> List[Dict[str, Any]]:
        """Extract COT data from OpenBB result."""
        try:
            df = result.to_df() if hasattr(result, 'to_df') else result
            if df is None or df.empty:
                return []

            data = []
            for _, row in df.iterrows():
                data.append({
                    "date": row.get("date", datetime.now()),
                    "market": row.get("market_name", ""),
                    "non_commercial_long": int(row.get("non_commercial_long", 0)),
                    "non_commercial_short": int(row.get("non_commercial_short", 0)),
                    "commercial_long": int(row.get("commercial_long", 0)),
                    "commercial_short": int(row.get("commercial_short", 0)),
                    "open_interest": int(row.get("open_interest", 0))
                })
            return data
        except Exception:
            return []


# Singleton instance
_openbb_service: Optional[OpenBBService] = None


def get_openbb_service() -> OpenBBService:
    """Get or create OpenBB service singleton."""
    global _openbb_service
    if _openbb_service is None:
        _openbb_service = OpenBBService()
    return _openbb_service
