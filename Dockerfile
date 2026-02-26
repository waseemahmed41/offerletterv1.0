# Use Python 3.11 slim image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y \
        --no-install-recommends \
        gcc \
        g++ \
        libpq-dev \
        libreoffice \
        libreoffice-writer \
        fonts-liberation \
        fonts-dejavu-core \
        fonts-liberation2 \
        fonts-noto-cjk \
        fonts-noto-color-emoji \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Create media directory
RUN mkdir -p /app/media/templates

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/admin/ || exit 1

# Run Gunicorn
CMD ["gunicorn", "--config", "gunicorn_config.py", "offer_automation.wsgi:application"]
