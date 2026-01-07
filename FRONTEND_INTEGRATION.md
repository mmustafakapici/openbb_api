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

## 🛠️ Temel Özellikler (Frontend İpuçları)

### 1. Alan Filtreleme (Field Filtering)
Daha az veri tüketmek istiyorsanız, sadece ihtiyacınız olan alanları isteyebilirsiniz:
`GET /yfinance/quote?symbol=AAPL&fields=symbol,price,change`

### 2. Önbellek (Caching)
Cevaplardaki `X-Cache` header'ını kontrol ederek verinin önbellekten gelip gelmediğini görebilirsiniz:
- `X-Cache: HIT` (Önbellekten geldi, süper hızlı)
- `X-Cache: MISS` (Yeni çekildi)

---

## 📍 En Önemli Endpoint Listesi

### 📈 Hisse Senedi & Yatırım Araçları (YFinance)
| Endpoint | Method | Açıklama |
| :--- | :--- | :--- |
| `/yfinance/quote` | `GET` | Anlık hisse fiyatı ve değişim verileri. |
| `/yfinance/historical` | `GET` | Geçmiş veriler (OHLCV). Pagination desteği var. |
| `/yfinance/profile` | `GET` | Şirket künyesi, açıklamalar ve sektör bilgisi. |
| `/yfinance/batch/quotes` | `POST` | **Toplu İstek:** `{"symbols": ["AAPL", "TSLA"]}` |
| `/yfinance/screener/gainers`| `GET` | Günün en çok kazandıran hisseleri. |

### 💎 Kripto & Döviz
| Endpoint | Method | Açıklama |
| :--- | :--- | :--- |
| `/yfinance/crypto/quote` | `GET` | Kripto fiyat verileri (Örn: BTC-USD). |
| `/yfinance/currency/quote`| `GET` | Forex parite verileri (Örn: EURUSD=X). |
| `/ecb/forex` | `GET` | **Yeni:** Avrupa Merkez Bankası döviz kurları. |

### 🛠️ Gelişmiş Finansal Veriler
| Endpoint | Method | Açıklama |
| :--- | :--- | :--- |
| `/cboe/options/chains` | `GET` | **Yeni:** Opsiyon zinciri verileri (Strike, IV, OI). |
| `/cftc/cot` | `GET` | **Yeni:** Piyasa pozisyon raporları (Komitman raporları). |
| `/sec/filings` | `GET` | Şirket resmi bildirimleri (10-K, 10-Q vb.). |

---

## 📦 Veri Şemaları (TypeScript İçin Taslaklar)

Frontend tarafında kullanabileceğiniz temel model yapıları şöyledir:

### 1. Hisse Fiyat Şeması (`EquityQuoteResponse`)
```typescript
interface EquityQuote {
  symbol: string;         // Örn: "AAPL"
  name: string;           // Şirket Adı
  price: number;          // Mevcut Fiyat
  change: number;         // Günlük Değişim ($)
  change_percent: number; // Günlük Değişim (%)
  volume: number;         // İşlem Hacmi
  market_cap: number;     // Piyasa Değeri
  last_updated: string;   // ISO 8601 Tarih
}
```

### 2. Opsiyon Şeması (`OptionsChainResponse`)
```typescript
interface OptionsChain {
  expiration: string;     // Vade Tarihi
  strike: number;         // Kullanım Fiyatı
  option_type: string;    // "call" veya "put"
  last_price: number;
  bid: number;
  ask: number;
  volume: number;
  open_interest: number;
  implied_volatility: number;
}
```

### 3. COT Raporu Şeması (`COTReportResponse`)
```typescript
interface COTReport {
  date: string;
  market: string;
  non_commercial_long: number;
  non_commercial_short: number;
  commercial_long: number;
  commercial_short: number;
  open_interest: number;
}
```

---

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
