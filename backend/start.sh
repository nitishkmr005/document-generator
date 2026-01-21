#!/bin/bash
# Startup script for Render deployment
# Optimized for fast startup - skips slow import tests

# Ensure output is not buffered
export PYTHONUNBUFFERED=1

# Use PORT from environment or default to 8000
PORT=${PORT:-8000}

echo "==> Starting PrismDocs API on port $PORT..."
echo "==> PYTHONPATH: $PYTHONPATH"
echo "==> Working directory: $(pwd)"
echo "==> Python version: $(python --version)"

# Ensure data directories exist
echo "==> Ensuring data directories exist..."
mkdir -p data/cache data/output data/temp data/logging 2>/dev/null || true

# Verify config file exists
if [ ! -f "/app/config/settings.yaml" ]; then
    echo "ERROR: Config file not found at /app/config/settings.yaml"
    exit 1
fi
echo "==> Config file found"

# Start uvicorn immediately - no slow import tests
# Heavy ML dependencies are loaded when first request comes in
echo "==> Starting uvicorn on 0.0.0.0:$PORT..."
exec python -m uvicorn doc_generator.infrastructure.api.main:app \
    --host 0.0.0.0 \
    --port "$PORT" \
    --log-level info \
    --access-log
