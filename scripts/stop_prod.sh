#!/bin/bash

# OpenBB Mobile API - Production Stop Script

# Proje dizinine git
cd "$(dirname "$0")/.."

# PID dosyasını kontrol et
if [ -f "logs/api.pid" ]; then
    PID=$(cat logs/api.pid)
    echo "API durduruluyor (PID: $PID)..."
    kill $PID && rm logs/api.pid
    echo "✅ API durduruldu."
else
    # PID dosyası yoksa süreci isme göre bul ve öldür
    echo "PID dosyası bulunamadı, süreci isme göre arıyorum..."
    pkill -f "uvicorn app.main:app" && echo "✅ API süreci durduruldu." || echo "❌ Çalışan bir API süreci bulunamadı."
fi
