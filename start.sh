#!/bin/bash
# OpenBB Mobile API - Linux/Mac Start Script

echo "Starting OpenBB Mobile API..."
echo ""

# Check if conda environment exists
if ! conda env list | grep -q "openbb"; then
    echo "Error: 'openbb' conda environment not found!"
    echo "Please create it first: conda create -n openbb python=3.11"
    exit 1
fi

# Activate conda environment
eval "$(conda shell.bash hook)"
conda activate openbb

# Change to script directory
cd "$(dirname "$0")"

# Check if port 8007 is in use
if lsof -Pi :8007 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "Warning: Port 8007 is already in use!"
    echo "Please close the application using that port."
    exit 1
fi

# Start the API
echo "Starting API on http://localhost:8007"
echo "Docs: http://localhost:8007/docs"
echo ""
echo "Press Ctrl+C to stop"
echo ""

uvicorn app.main:app --host 0.0.0.0 --port 8007 --reload --workers 4
