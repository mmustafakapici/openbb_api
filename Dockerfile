# OpenBB Mobile API - Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy OpenBB environment (already installed)
COPY openbb_env /openbb_env

# Set environment variables
ENV PATH="/openbb_env/Scripts:${PATH}"
ENV PYTHONPATH="/openbb_env/Lib/site-packages:${PYTHONPATH}"
ENV OPENBB_USER_DATA_PATH="/app/.openbb_platform"

# Copy application code
COPY openbb_mobile_api /app

# Install application dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Create directory for OpenBB user data
RUN mkdir -p /app/.openbb_platform

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
