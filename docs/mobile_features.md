# 📱 OpenBB Mobile App - Uygulama Özellikleri & Vizyon Rehberi

Bu döküman, elimizdeki API verilerini kullanarak bir mobil uygulamada hangi "katil özellikleri" (killer features) geliştirebileceğimizi ve kullanıcıya nasıl bir değer sunabileceğimizi özetler.

---

## 🔝 1. Ana Dashboard (Piyasa Özeti)
Uygulamanın açılış ekranı. API'deki `batch/quotes` ve `screener` endpoint'lerini kullanarak:
- **Günün Özeti:** En çok yükselen (gainers) ve düşen (losers) hisseler/kriptolar.
- **Canlı İzleme Listesi:** Kullanıcının takip ettiği varlıkların anlık fiyatları (`batch/quotes` ile tek istekte 50+ varlık).
- **Korku & Açgözlülük Göstergesi:** Fed faiz oranları (`fed/federal/funds/rate`) ve Hazine verimleri ile piyasa risk algısını görselleştirme.

---

## 🕯️ 2. Gelişmiş Grafik & Teknik Analiz
`historical` endpoint'lerinden gelen verilerle:
- **İnteraktif OHLCV Grafikleri:** Mum grafikler üzerinden geçmişe dönük analiz.
- **Performans Karşılaştırma:** Bir hisse ile bir ETF'yi (Örn: AAPL vs QQQ) aynı grafikte kıyaslama.
- **Zaman Yolculuğu:** 1Y, 5Y veya Max verilerle uzun vadeli trend analizi.

---

## 🔎 3. Şirket Derin Dalış (Deep Dive)
`profile` ve `sec/filings` verilerini birleştirerek:
- **Şeffaf Şirket Kartı:** Şirket ne iş yapar? Hangi sektörde? Web sitesi ve yönetim ekibi kim?
- **Resmi Bildirim Takvimi:** SEC'e iletilen en son 10-K (yıllık) ve 10-Q (çeyreklik) raporlarının linkleri ve tarihleri.
- **İçeriden Bilgi (Insider Trading):** *Şirket CEO'su kendi hissesini mi satıyor?* `sec/insider/trading` verisiyle güven puanı oluşturma.

---

## 🎲 4. Opsiyon Stratejileri (Professional Mode)
Yeni eklediğimiz `cboe/options/chains` endpoint'i ile:
- **Opsiyon Zinciri Görünümü:** Belirli bir hissenin tüm vade tarihlerindeki Call/Put opsiyonlarını listeleme.
- **IV (Implied Volatility) Takibi:** Hangi opsiyonlar "pahalı", hangileri "ucuz"?
- **Greeks (Beta/Delta) Görselleştirme:** Yatırımcıların beklediği fiyat hareketlerini ısı haritası (heat map) ile gösterme.

---

## 🏛️ 5. Makro Ekonomi Takibi
`fed` ve `ecb` verileriyle:
- **Merkez Bankası İzleme:** Fed ve ECB faiz kararları öncesi mevcut oranların takibi.
- **Faiz Eğrisi (Yield Curve) Analizi:** Durgunluk (recession) sinyallerini (2Y vs 10Y verim farkı) otomatik hesaplayan bir widget.
- **Enflasyon & Büyüme:** Makro verilerle yatırım stratejisini güncelleme.

---

## 🐂 6. Akıllı Para Takibi (Smart Money - COT)
`cftc/cot` verisiyle:
- **Kurumsal vs Bireysel:** Büyük kurumsal yatırımcılar (Commercials) ne yönde pozisyon alıyor?
- **Piyasa Duyarlılığı:** Altın, Petrol veya S&P 500 gibi emtia ve endekslerdeki "Net Long/Short" pozisyonları grafikleştirme. Kurumsal yatırımcılar long'da ise yükseliş beklentisi!

---

## 🔔 7. Akıllı Bildirimler (Push Notifications)
(Backend yardımıyla yapılabilecekler):
- **SEC Alert:** Takip ettiğin şirket yeni bir 10-K raporu yayınladığında anında bildirim.
- **Volatility Alert:** IV (Zımni Oynaklık) %20 arttığında veya faiz oranları değiştiğinde uyarı.
- **Whale Alert:** Büyük bir insider trading (CEO alışı vb.) olduğunda "Balinalar alıyor!" bildirimi.

---

## 🧩 8. Mobil Widget'lar (iOS & Android)
Uygulamayı açmadan değer sunan, ekranın en değerli yerine kurulan mini araçlar:
- **Hızlı Takip (Small Widget):** Tek bir varlığın (Örn: BTC veya Altın) anlık fiyatı ve günlük değişim yüzdesi.
- **Portföy Özeti (Medium Widget):** Kullanıcının en çok takip ettiği 3 varlık ve Fed faiz oranı.
- **Resesyon Radarı (Wide Widget):** Yield Curve (Verim Eğrisi) grafiği. Eğer eğri tersine dönerse (2Y > 10Y) widget kırmızı yanar. Kurumsal kullanıcılar buna bayılır.
- **Döviz Çevirici (Interactive Widget):** `ecb/forex` verisiyle kilit ekranından hızlıca kur hesaplama.

---

## ⌚ 9. Apple Watch & Companion (Giyilebilir)
- **Komplikasyonlar (Complications):** Saat kadranında tek bakışta görülebilen anlık hisse fiyatı.
- **Hızlı Uyarılar:** Büyük fiyat hareketlerinde saatte titreşimli bildirim.

---

## 💡 Frontendci İçin Tasarım İpucu
- **Karanlık Mod (Dark Mode):** Finans uygulamalarında "Bloomberg Terminal" hissi veren koyu temalar çok popülerdir (Koyu gri/Siyah arka plan + Neon Yeşil/Kırmızı vurgular).
- **Hızlı Erişim:** Ana sayfada tek tıkla `batch` data çekerek uygulamanın çok hızlı (snappi) hissettirilmesi.

---
*OpenBB Mobile App Strategy v1.0*
