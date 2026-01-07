# 📱 OpenBB Mobile API - Frontend Entegrasyon Rehberi

Bu döküman, OpenBB Mobile API'yi frontend projene entegre etmen için gereken tüm teknik detayları ve veri şemalarını içerir.

## 🚀 Genel Bilgiler
- **Local Base URL:** `http://localhost:8007` (Geliştirme aşaması)
- **Production Base URL:** `http://<ELASTIC-IP-ADRESINIZ>:8007` (Canlı ortam - EC2 / Oracle)
- **API Prefix:** `/api/v2/mobile`
- **İnteraktif Swagger Docs:** `/docs` (Base URL sonuna ekleyin)
- **Özellikler:** Hafifletilmiş JSON (Mobile Friendly), Smart Caching (TTL: 1-15dk), Field Filtering.

---

## 🌐 Ortam Yönetimi (Frontend İçin)

Frontend projenizde ortam değişikliğini (Local vs Production) yönetmek için genellikle `.env` dosyası kullanılır:

```javascript
// .env.development
VITE_API_URL=http://localhost:8007/api/v2/mobile

// .env.production
VITE_API_URL=http://<YOUR-EC2-ELASTIC-IP>:8007/api/v2/mobile
```

> **Önemli:** Eğer EC2 üzerine Nginx ve SSL kurduysanız, production URL'iniz `https://api.domaininiz.com/api/v2/mobile` şeklinde olacaktır. Mobil cihazlar ve modern tarayıcılar için **HTTPS** kullanımı şiddetle önerilir.

---

## 📍 Terminal (Endpoint) Listesi

Tüm endpoint'ler `/api/v2/mobile` prefix'i ile başlar.

### 📈 Hisse Senedi & Yatırım Araçları (Equity & ETF)
| Endpoint | Method | Sağlayıcı | Açıklama |
| :--- | :--- | :--- | :--- |
| `/yfinance/quote` | `GET` | YFinance | Anlık hisse fiyatı ve temel istatistikler. |
| `/yfinance/historical` | `GET` | YFinance | Geçmiş OHLCV verileri (Günlük/Haftalık). |
| `/yfinance/profile` | `GET` | YFinance | Şirket künyesi (Sektör, Sanayi, Web sitesi). |
| `/yfinance/batch/quotes` | `POST` | YFinance | Çoklu hisse senedi/kripto fiyat çekme. |
| `/yfinance/screener/gainers`| `GET` | YFinance | Günün en çok değer kazananları. |
| `/yfinance/etf/info` | `GET` | YFinance | ETF detayları (Gider oranı, AUM, NAV). |
| `/sec/filings` | `GET` | SEC | Şirket resmi bildirimleri (10-K, 10-Q). |
| `/sec/insider/trading` | `GET` | SEC | Kurumsal/İçeriden ticaret işlemleri. |

### 💎 Kripto, Döviz & Opsiyonlar
| Endpoint | Method | Sağlayıcı | Açıklama |
| :--- | :--- | :--- | :--- |
| `/yfinance/crypto/quote` | `GET` | YFinance | Kripto fiyat (Market Cap, 24h Change). |
| `/yfinance/currency/quote`| `GET` | YFinance | Forex parite (Örn: EURUSD=X). |
| `/ecb/forex` | `GET` | ECB | Avrupa Merkez Bankası döviz kurları. |
| `/cboe/options/chains` | `GET` | CBOE | Opsiyon zinciri (Strike, IV, OI). |
| `/cftc/cot` | `GET` | CFTC | Komitman pozisyon raporları. |

### 🏛️ Ekonomi (Macro)
| Endpoint | Method | Sağlayıcı | Açıklama |
| :--- | :--- | :--- | :--- |
| `/fed/treasury/rates` | `GET` | Fed | Hazine faiz oranları (1A - 30Y). |
| `/fed/federal/funds/rate`| `GET` | Fed | Federal Fon Oranı (FFR). |
| `/fed/sofr/rate` | `GET` | Fed | SOFR (Overnight Financing Rate). |
| `/fed/yield/curve` | `GET` | Fed | Verim eğrisi (Yield Curve) veri noktaları. |

---

## 📦 Veri Şemaları (TypeScript Model)

### 1. Fiyat Bilgisi (`EquityQuoteResponse`)
```typescript
interface EquityQuote {
  symbol: string;
  name?: string;
  price: number;
  change: number;
  change_percent: number;
  volume?: number;
  market_cap?: number;
  last_updated: string; // ISO 8601
}
```

### 2. Kripto Bilgisi (`CryptoQuoteResponse`)
```typescript
interface CryptoQuote {
  symbol: string;
  name?: string;
  price: number;
  change_24h: number;
  change_percent_24h: number;
  volume_24h?: number;
  market_cap?: number;
  last_updated: string;
}
```

### 3. Opsiyon Zinciri (`OptionsChainResponse`)
```typescript
interface OptionsChain {
  expiration: string;
  strike: number;
  option_type: "call" | "put";
  last_price?: number;
  bid?: number;
  ask?: number;
  volume?: number;
  open_interest?: number;
  implied_volatility?: number;
}
```

### 4. Ekonomi/Faiz (`TreasuryRateResponse`)
```typescript
interface TreasuryRate {
  maturity: string; // Örn: "10Y"
  rate: number;
  date: string;
}
```

---

## 📄 Sayfalama (Pagination)
Historical veri dönen endpoint'lerde response şu yapıdadır:

```typescript
interface PaginatedResponse<T> {
  data: T[];
  pagination: {
    page: number;
    limit: number;
    total: number;
    total_pages: number;
    has_next: boolean;
    has_prev: boolean;
  }
}
```

---

## 🏁 Genel Durum & Sürüm
Sistemin ayakta olup olmadığını kontrol etmek için:
`GET /health`

Cevap:
```json
{
  "status": "ok",
  "version": "2.0.0",
  "cache_enabled": true
}
```

## ⚠️ Hata Yönetimi
Hata durumunda (4xx veya 5xx) API şu formatta bir cevap döner:
```json
{
  "success": false,
  "error": "INTERNAL_ERROR",
  "detail": "Hatanın teknik açıklaması burada yer alır."
}
```

---
*OpenBB Mobile API v2.0.0*
