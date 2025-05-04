# for render deployment
# Base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies for MySQL client and build tools
RUN apt-get update && \
    apt-get install -y build-essential default-libmysqlclient-dev pkg-config && \
    rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install gunicorn

# Copy project source (includes entrypoint scripts)
COPY . .

# Make entrypoints executable
RUN chmod +x /app/docker/django/entrypoint.sh \
    && chmod +x /app/docker/celery/worker_entrypoint.sh \
    && chmod +x /app/docker/celery/beat_entrypoint.sh

# Default entrypoint triggers Django entrypoint script
ENTRYPOINT ["sh", "/app/docker/django/entrypoint.sh"]



# original for Docker coompose runnig
# # Base image
# FROM python:3.11-slim

# # Set working directory
# WORKDIR /app

# # Install system dependencies for MySQL client and build tools
# RUN apt-get update && \
#     apt-get install -y build-essential default-libmysqlclient-dev pkg-config && \
#     rm -rf /var/lib/apt/lists/*

# # Copy and install Python dependencies
# COPY requirements.txt .
# RUN pip install --upgrade pip \
#     && pip install --no-cache-dir -r requirements.txt

# # Ensure gunicorn is installed
# # (requirements.txt should include: gunicorn)
# # If it’s missing, install explicitly:
# RUN pip install gunicorn

# # Copy project source
# COPY . .

# # Make entrypoints executable
# RUN chmod +x docker/django/entrypoint.sh \
#     && chmod +x docker/celery/worker_entrypoint.sh \
#     && chmod +x docker/celery/beat_entrypoint.sh

# # Default entrypoint
# ENTRYPOINT ["sh", "docker/django/entrypoint.sh"]