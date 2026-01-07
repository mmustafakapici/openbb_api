# 🚀 AWS Deployment Stratejisi: Çoklu Client (Mobil, Web, Desktop) Desteği

Bu rehber, OpenBB Mobile API'yi Mobil Uygulama, Web Sitesi ve Desktop Uygulaması (Electron vb.) için merkezi bir backend olarak AWS üzerinde nasıl konumlandıracağınızı açıklar.

---

## 📊 AWS Deployment Yöntemleri Karşılaştırması

| Özellik | **Option A: AWS App Runner** (En Modern/Kolay) | **Option B: AWS EC2** (En Klasik/Ucuz) | **Option C: AWS Lightsail** (En Tahmin Edilebilir) |
| :--- | :--- | :--- | :--- |
| **Zorluk Seviyesi** | ⭐ (Çok Kolay) | ⭐⭐⭐ (Orta - Sunucu yönetimi ister) | ⭐⭐ (Kolay) |
| **SSL/HTTPS** | ✅ **Otomatik Dahil** | ❌ Manuel (Certbot/Nginx ister) | ✅ Basitleştirilmiş Panelden |
| **Ölçeklenebilirlik**| ✅ Otomatik (Gelen yüke göre artar) | ❌ Manuel müdahale ister | ❌ Sınırlı |
| **Maliyet Yapısı** | Kullandığın kadar (Pay-as-you-go) | Free Tier (12 ay bedava) yoksa sabit | Sabit Aylık Fiyat ($3.50'dan başlar) |
| **Bakım Yükü** | Sıfır (Serverless) | OS Update + Security Yamaları ister | Düşük |
| **Çoklu Client** | 🚀 **Mükemmel** (Dahili HTTPS & CORS) | 🛠️ Yapılandırma Gerektirir | ✅ Uygun |

---

## 🏗️ Çoklu Client Mimarisi İçin Gereksinimler

Mobil, Web ve Desktop uygulamalarınızın bu API'ye sorunsuz bağlanması için AWS'de şu 3 şeyi doğru yapmalısınız:

### 1. CORS Ayarları (Web Sitesi İçin Şart)
Web siteniz API'\\ye istek attığında tarayıcı güvenliği (CORS) engeline takılmamak için `app/config.py` içinde `CORS_ORIGINS` kısmına sitenizin adresini ekleyin.
*   **Lightsail/EC2'de:** Nginx konfigürasyonunda `Access-Control-Allow-Origin` set edilmelidir.
*   **App Runner'da:** Otomatik halledilir.

### 2. HTTPS (Mobil ve Modern Browserlar İçin Şart)
*   **Android/iOS:** Güvenli olmayan (HTTP) bağlantıları varsayılan olarak engeller.
*   **Çözüm:** App Runner kullanırsanız AWS size otomatik Amazon onaylı SSL verir. EC2 kullanırsanız "Let's Encrypt" kurmanız gerekir.

### 3. Static IP / Elastic IP (Desktop ve Mobil İçin Şart)
Uygulamanızın içine gömeceğiniz API adresi sürekli değişmemeli.
*   **EC2:** Mutlaka bir "Elastic IP" atanmalıdır.
*   **App Runner:** Size kalıcı bir domain (zxcvbnm.awsapprunner.com gibi) verir.

---

## 🛠️ Adım Adım En Kolay Deployment (App Runner Yöntemi)

Backend yönetimiyle uğraşmak istemeyen ve 3 client'a da hızlıca hizmet vermek isteyenler için:

1.  **GitHub Bağlantısı:** API kodlarını GitHub'a yükleyin.
2.  **Service Oluşturma:** AWS App Runner paneline gidin -> "Create Service".
3.  **Kaynak:** Kod kaynağı olarak GitHub Reponuzu seçin.
4.  **Runtime Ayarları:**
    - `Runtime`: Python 3
    - `Build command`: `pip install -r requirements.txt`
    - `Start command`: `uvicorn app.main:app --host 0.0.0.0 --port 8007`
    - `Port`: 8007
5.  **Otomatik Deploy:** "Deployment settings" -> "Automatic" seçin. (Siz koda her 'push' attığınızda sunucu kendini günceller).

---

## 🛠️ Klasik ve Ekonomik Deployment (AWS EC2 Yöntemi)

Eğer "Free Tier" kullanmak veya sunucu üzerinde tam kontrole sahip olmak istiyorsanız:

### 1. Instance Hazırlığı
1. **Launch Instance:** AWS EC2 paneline gidin, **Ubuntu 24.04 LTS** (veya 22.04) seçin.
2. **Instance Type:** Ücretsiz katman için `t3.micro` veya `t2.micro` seçin.
3. **Key Pair:** SSH ile bağlanmak için anahtarınızı oluşturun/seçin.
4. **Network Settings (Security Group):** 
   - SSH (Port 22) - Kendi IP'nize izin verin.
   - Custom TCP (Port 8007) - `0.0.0.0/0` (API için).
   - HTTP (Port 80) ve HTTPS (Port 443) - `0.0.0.0/0` (Nginx için).

### 2. Sabit IP Atama (Elastic IP)
EC2 sunucuları yeniden başlatıldığında IP'leri değişebilir. Desktop ve mobil uygulamaların adresi unutmaması için:
1. EC2 Paneli -> **Elastic IPs** -> **Allocate Elastic IP**.
2. Oluşan IP'ye sağ tıklayıp **Associate Elastic IP** diyerek sunucunuzu seçin.

### 3. Sunucu Kurulumu (SSH)
Terminalden sunucunuza bağlanın:
```bash
ssh -i "key.pem" ubuntu@elastic-ip-adresiniz

# Sistemi Güncelle ve Docker Yükle
sudo apt update && sudo apt upgrade -y
sudo apt install docker.io docker-compose -y

# Uygulamayı Çek
git clone <repo-url>
cd openbb_api

# Docker ile Çalıştır
sudo docker-compose up -d
```

### 4. (Opsiyonel ama Önerilen) Nginx + SSL Kurulumu
Mobil uygulamalar için HTTPS zorunludur. `certbot` ile ücretsiz SSL alabilirsiniz:
```bash
sudo apt install nginx python3-certbot-nginx -y
# Nginx konfigürasyonunda 8007 portunu 80/443'e yönlendirin.
sudo certbot --nginx -d yourdomain.com
```

---

## 💰 Maliyet Optimizasyonu İpucu
Eğer projeniz henüz başlangıç aşamasındaysa ve çok trafik almıyorsa:
*   **App Runner**'da "Provisioned Instances" değerini **0** yapın. Böylece uygulama kullanılmadığında CPU ücreti ödemezsiniz (Sadece RAM ücreti, aylık ~$7).
*   **EC2 t3.micro** kullanırsanız (12 ay bedava) aylık maliyetiniz **$0** olur.

---
*OpenBB API - Deployment Strategy v1.0*
