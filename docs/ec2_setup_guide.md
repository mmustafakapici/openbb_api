# 🌐 AWS EC2 Micro (Ubuntu) Kurulum Rehberi

Bu rehber, AWS EC2 üzerinde **t2.micro** veya **t3.micro** (1GB RAM) özellikli bir Ubuntu sunucuda OpenBB Mobile API'yi sıfırdan nasıl kuracağınızı anlatır.

---

## 🏗️ 1. RAM Takviyesi (Swap Memory)
EC2 Micro sunucular 1GB RAM'e sahiptir. Paket yüklemeleri sırasında makinenin donmaması için 2GB Sanal RAM ekliyoruz:

```bash
# Sistemi güncelle
sudo apt update && sudo apt upgrade -y

# 2GB Swap dosyası oluştur
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# Kalıcı hale getir (reboot sonrası çalışması için)
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

---

## 🐍 2. Python ve Gerekli Araçların Kurulumu
Ubuntu üzerinde projemizi çalıştırmak için gerekli paketleri yüklüyoruz:

```bash
# Python, Pip ve Sanal Ortam (venv) kurulumu
sudo apt install git python3-pip python3-venv screen -y

# Python versiyon kontrolü
python3 --version
```

---

## 📂 3. Projenin Kurulması
Projeyi GitHub üzerinden çekip bağımlılıkları yüklüyoruz:

```bash
# Projeyi klonla
git clone https://github.com/kullanici_adin/openbb_api.git
cd openbb_api

# Sanal ortam oluştur ve aktifleştir
python3 -m venv venv
source venv/bin/activate

# Bağımlılıkları yükle
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 🚀 4. API'yi Arka Planda Çalıştırma (Screen)
Uzak terminali kapatsanız bile API'nin çalışmaya devam etmesi için `screen` kullanıyoruz:

1. Yeni bir ekran açın:
   ```bash
   screen -S openbb_api
   ```
2. Sanal ortamı aktif edin (etmediyseniz):
   ```bash
   source venv/bin/activate
   ```
3. API'yi başlatın:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8007
   ```
4. **Oturumdan Ayrılın:** Klavyede `CTRL + A` tuşuna basıp hemen ardından `D` tuşuna basın. (Detached)

> **Geri bağlanmak için:** `screen -r openbb_api` komutunu kullanabilirsiniz.

---

## 🔒 5. AWS Güvenlik Grubu (Security Group) Ayarı
API'ye dışarıdan erişebilmek için AWS Dashboard üzerinden şu portu açmalısınız:

1. **Inbound Rules** -> **Edit Inbound Rules**.
2. **Type:** `Custom TCP` | **Port Range:** `8007` | **Source:** `0.0.0.0/0`.
3. Ayarları kaydedin.

---

## 🌍 6. API'ye Erişim
Kurulum bittikten sonra API'nize şu adresten ulaşabilirsiniz:
`http://<AWS-ELASTIC-IP>:8007/docs`

---
*OpenBB API - EC2 Setup Guide v1.0*
