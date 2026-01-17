# AI Disease Detection Backend - Dockerfile
# Python 3.12.6 compatible

FROM python:3.12-slim

WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    TORCH_HOME=/app/.cache/torch

# Install system dependencies for OpenCV, PyTorch, and image processing
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    libglib2.0-0 \
    libgl1 \
    libglib2.0-dev \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Create necessary directories early
RUN mkdir -p static/heatmaps models uploads logs .cache/torch

# Copy application code
COPY . .

# Pre-build AI models during Docker build phase
# This moves the long download/setup process to build time
# Use --skip-verification to save memory during build
RUN python create_demo_models.py --skip-verification

# Copy entrypoint script
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

# Create necessary directories
RUN mkdir -p static/heatmaps models uploads logs

# Create non-root user for security
RUN adduser --disabled-password --gecos "" appuser && \
    chown -R appuser:appuser /app
USER appuser

# Expose port (default 8000, Render will override)
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Run the application through the entrypoint script
CMD ["./entrypoint.sh"]
