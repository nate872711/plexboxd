FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Working directory inside container
WORKDIR /app

# OS dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl wget tzdata \
    && rm -rf /var/lib/apt/lists/*

# Copy real application code (your actual structure)
COPY ./app/src /app/src

# Copy dependency list
COPY ./requirements.txt /app/requirements.txt

# Install dependencies — ALWAYS installs required packages
RUN pip install --no-cache-dir -r /app/requirements.txt || true
RUN pip install --no-cache-dir \
        pyyaml \
        requests \
        python-dotenv \
        rich \
        fastapi \
        uvicorn[standard] \
        plexapi \
        trakt.py \
        beautifulsoup4 \
        lxml \
        pandas \
        tmdbsimple \
        tvdb-v4 \
        httpx \
        apscheduler

# Create persisted folders
RUN mkdir -p /config /logs

EXPOSE 8089

# Start WatchWeave
CMD ["python", "-u", "/app/src/main.py"]
