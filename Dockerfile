# Use Python 3.11 slim image for smaller size
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies for PDF/image processing
RUN apt-get update && apt-get install -y \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    shared-mime-info \
    && rm -rf /var/lib/apt/lists/*

# Install uv for fast dependency installation
RUN pip install --no-cache-dir uv

# Copy dependency files first (for layer caching)
COPY pyproject.toml ./

# Install dependencies using uv
RUN uv pip install --system --no-cache .

# Copy source code
COPY src/ ./src/
COPY scripts/ ./scripts/
COPY config/ ./config/

# Create directories for input/output
RUN mkdir -p src/data src/output

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Default command
ENTRYPOINT ["python", "scripts/run_generator.py"]
CMD ["--help"]
