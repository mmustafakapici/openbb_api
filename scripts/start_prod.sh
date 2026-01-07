#!/bin/bash

# OpenBB Mobile API - Production Start Script
# Bu script API'yi arka planda (background) çalıştırır ve logları kaydeder.

# Proje dizinine git
cd "$(dirname "$0")/.."

# Sanal ortam kontrolü
if [ ! -d "venv" ]; then
    echo "Hata: 'venv' klasörü bulunamadı. Lütfen önce kurulumu tamamlayın."
    exit 1
fi

# Çalışan eski bir süreç varsa durdur
echo "Eski süreçler kontrol ediliyor..."
pkill -f "uvicorn app.main:app" || echo "Çalışan süreç bulunamadı."

# Log dizini oluştur
mkdir -p logs

# API'yi nohup ile arka planda başlat
echo "API arka planda başlatılıyor (Port 8007)..."
nohup venv/bin/python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8007 --workers 4 > logs/api.log 2>&1 &

# Yeni PID'yi kaydet
echo $! > logs/api.pid

echo "✅ API başlatıldı!"
echo "Logları izlemek için: tail -f logs/api.log"
echo "API'yi durdurmak için: ./scripts/stop_prod.sh"
