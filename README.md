# OpenBB Mobile API

Mobile-optimized FastAPI backend for financial data using OpenBB Platform's free providers.

## Features

- ✅ **No API Keys Required** - Uses YFinance, Federal Reserve, SEC providers
- ✅ **Mobile Optimized** - Lightweight responses (5-10 fields vs 50+)
- ✅ **Smart Caching** - In-memory cache with optional Redis
- ✅ **Batch Requests** - Fetch multiple quotes in one call
- ✅ **Docker Ready** - Single command deployment
- ✅ **OpenAPI Docs** - Built-in Swagger documentation

## Quick Start

### Option 1: Start Script (Recommended)

**Windows:**
```bash
cd openbb_mobile_api
start.bat
```

**Linux/Mac:**
```bash
cd openbb_mobile_api
chmod +x start.sh
./start.sh
```

API will be available at http://localhost:8007

### Option 2: Using Docker

```bash
cd openbb_mobile_api
docker-compose up -d

# API at http://localhost:8000
# Docs at http://localhost:8000/docs
```

### Option 3: Manual Installation

```bash
# Activate conda environment
conda activate openbb

# Install dependencies
pip install -r openbb_mobile_api/requirements.txt

# Run the API
cd openbb_mobile_api
uvicorn app.main:app --host 0.0.0.0 --port 8007 --reload
```

## API Endpoints

### Equity (YFinance)

```
GET  /api/v2/mobile/yfinance/quote                    # Stock quote
GET  /api/v2/mobile/yfinance/historical               # Historical prices
GET  /api/v2/mobile/yfinance/profile                  # Company profile
GET  /api/v2/mobile/yfinance/screener/gainers         # Top gainers
GET  /api/v2/mobile/yfinance/screener/losers          # Top losers
POST /api/v2/mobile/yfinance/batch/quotes             # Batch quotes
```

### Crypto (YFinance)

```
GET  /api/v2/mobile/yfinance/crypto/quote             # Crypto quote
GET  /api/v2/mobile/yfinance/crypto/historical        # Crypto historical
```

### Economy (Federal Reserve)

```
GET  /api/v2/mobile/fed/treasury/rates                # Treasury rates
GET  /api/v2/mobile/fed/federal/funds/rate            # Fed funds rate
GET  /api/v2/mobile/fed/sofr/rate                     # SOFR rate
```

### Regulators (SEC)

```
GET  /api/v2/mobile/sec/filings                       # SEC filings
GET  /api/v2/mobile/sec/insider/trading               # Insider trading
```

### Currency (YFinance)

```
GET  /api/v2/mobile/yfinance/currency/quote           # Forex quote
GET  /api/v2/mobile/yfinance/currency/historical      # Forex historical
```

### ETF (YFinance)

```
GET  /api/v2/mobile/yfinance/etf/info                 # ETF info
GET  /api/v2/mobile/yfinance/etf/historical           # ETF historical
```

## Example Usage

### Get Stock Quote

```bash
curl "http://localhost:8000/api/v2/mobile/yfinance/quote?symbol=AAPL"
```

Response:
```json
{
  "symbol": "AAPL",
  "name": "Apple Inc.",
  "price": 185.92,
  "change": 0.45,
  "change_percent": 0.24,
  "volume": 52341234,
  "market_cap": 2900000000000,
  "last_updated": "2024-01-15T10:35:00"
}
```

### Batch Quotes

```bash
curl -X POST "http://localhost:8000/api/v2/mobile/yfinance/batch/quotes" \
  -H "Content-Type: application/json" \
  -d '{"symbols": ["AAPL", "GOOGL", "MSFT"]}'
```

### Historical Data with Pagination

```bash
curl "http://localhost:8000/api/v2/mobile/yfinance/historical?symbol=AAPL&start_date=2024-01-01&end_date=2024-01-31&page=1&limit=50"
```

### Crypto Quote

```bash
curl "http://localhost:8000/api/v2/mobile/yfinance/crypto/quote?symbol=BTC-USD"
```

### Treasury Rates

```bash
curl "http://localhost:8000/api/v2/mobile/fed/treasury/rates"
```

## Mobile Optimization

### Field Filtering

Request only the fields you need:

```bash
curl "http://localhost:8000/api/v2/mobile/yfinance/quote?symbol=AAPL&fields=symbol,price,change"
```

### Pagination

All list endpoints support pagination:

- `page`: Page number (default: 1)
- `limit`: Items per page (default: 50, max: 200)

### Compression

Responses > 1KB are automatically GZip compressed.

## Configuration

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

Key settings:
- `CACHE_ENABLED`: Enable/disable caching (default: true)
- `REDIS_HOST`: Redis server host (default: localhost)
- `CORS_ORIGINS`: Allowed CORS origins (default: *)

## Project Structure

```
openbb_mobile_api/
├── app/
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration
│   ├── models/              # Pydantic models
│   ├── routers/             # API endpoints
│   ├── services/            # Business logic
│   └── middleware/          # Custom middleware
├── requirements.txt         # Python dependencies
├── Dockerfile              # Docker image
├── docker-compose.yml      # Docker compose
└── README.md               # This file
```

## Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run with auto-reload
cd openbb_mobile_api
python -m app.main
```

API documentation available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Production Deployment

### Docker Compose (Recommended)

```bash
docker-compose up -d
```

### Manual with Uvicorn

**Linux/Mac (Multi-worker):**
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

**Windows (Single worker):**
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

**Development with auto-reload:**
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Environment Variables

Set these for production:

```bash
CORS_ORIGINS=https://your-mobile-app.com
CACHE_ENABLED=true
REDIS_HOST=redis-production
```

## License

AGPL-3.0

## Providers

| Provider | Data Type | API Key |
|----------|-----------|---------|
| YFinance | Equity, ETF, Crypto, Forex | ❌ No |
| Federal Reserve | Interest rates, economic | ❌ No |
| SEC | Filings, insider trading | ❌ No |
| FRED | Economic indicators | Free key |
| US EIA | Energy data | Free key |
| CFTC | Futures data | Free key |

## Support

- OpenBB Docs: https://docs.openbb.co
- GitHub Issues: https://github.com/OpenBB-finance/OpenBB/issues
