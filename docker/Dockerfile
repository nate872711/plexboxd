# ────────────────────────────────────────────────
# Flexboxd Dockerfile
# Supports Plex, Letterboxd, IMDb, and Trakt syncs
# ────────────────────────────────────────────────

FROM python:3.12-slim AS base

# Set environment defaults
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    APP_HOME=/app

WORKDIR $APP_HOME

# Install base packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    bash curl ca-certificates tini \
 && rm -rf /var/lib/apt/lists/*

# Copy requirements early to leverage caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy full application
COPY . .

# Add a non-root user for security
RUN useradd -m flexboxd
USER flexboxd

# Expose the default Flask/HTTP port for optional WebUI or API
EXPOSE 8089

# Use tini as init for clean signal handling
ENTRYPOINT ["/usr/bin/tini", "--"]

# Default command: run the main sync service
CMD ["python", "-m", "src.main"]
