# Base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y build-essential default-libmysqlclient-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project code
COPY app/ .
COPY docker/ ./docker/

# Make entrypoints executable
RUN chmod +x docker/django/entrypoint.sh docker/celery/worker_entrypoint.sh

# Default: run Django
ENTRYPOINT ["sh", "docker/django/entrypoint.sh"]