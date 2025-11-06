<p align="center">
<img src="/branding/plexboxd-banner.png" width="300">


# 🍿 Plexboxd
<div align="center">

[![Docker Pulls](https://img.shields.io/docker/pulls/nate8727/plexboxd?logo=docker&style=flat-square)](https://hub.docker.com/r/nate8727/plexboxd)
[![GitHub Release](https://img.shields.io/github/v/release/nate872711/plexboxd?logo=github&style=flat-square)](https://github.com/nate872711/plexboxd/releases)
[![Build & Release](https://github.com/nate872711/plexboxd/actions/workflows/release.yml/badge.svg)](https://github.com/nate872711/plexboxd/actions/workflows/release.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)
</div>

**Your Plex movies, your Letterboxd diary — finally in sync.**

**Plexboxd** is a self-hosted integration bridge between **Plex**, **Letterboxd**, **Trakt**, and **IMDb**.  
It syncs your watched movies and shows, updates your Letterboxd diary, manages watchlists and collections, and provides export/import utilities for your media ecosystem.

---

## 🚀 Features

| Feature | Description |
|----------|--------------|
| 🎞️ **Diary Sync** | Sync Plex watched activity to your Letterboxd diary |
| 🧾 **IMDb Sync** | Import IMDb ratings/watchlist CSVs and sync to Trakt or Letterboxd |
| 🔁 **Trakt Integration** | Pushes watched items, lists, and watchlists to Trakt |
| 📚 **Collections → Lists** | Map Plex collections directly to Trakt lists |
| 📊 **Sync History & Logs** | Tracks every synced item with timestamps |
| 💬 **Webhook Support** | Optional Discord or Slack notifications |
| 🐳 **Dockerized** | Easy to deploy and run as a lightweight container |

---

## 🛣️ Roadmap

- [ ] WebUI
- [ ] Two-way Letterboxd ↔ Plex sync  
- [ ] Local web dashboard with sync stats  
- [ ] Smart retry + failure queue system  
- [ ] Scheduled background sync intervals  

---

## 🧩 Supported Integrations

| Integration | Supported Operations |
|--------------|----------------------|
| **Letterboxd** | Diary sync (via CSV) |
| **Trakt.tv** | Watchlist + lists + watched sync |
| **IMDb** | Ratings and watchlist CSV import |
| **Plex** | Collections, watch states, metadata |
| **Webhook** | Notifications (optional) |

---

## Quick start (Docker)
```bash
cp .env.example .env
docker compose -f docker/docker-compose.yml up -d --build
```
### Clone the Repository
```bash
git clone https://github.com/nate872711/plexboxd.git
cd plexboxd
```
### Example docker compose
```yaml
services:
  plexboxd:
    container_name: plexboxd
    image: nate8727/plexboxd:latest
    build:
      context: ..
      dockerfile: docker/Dockerfile
    restart: unless-stopped
    environment:
      # Core configuration
      - TZ=UTC
      - PLEX_BASE_URL=${PLEX_BASE_URL}
      - PLEX_TOKEN=${PLEX_TOKEN}

      # Letterboxd CSV sync
      - CSV_PATH=${CSV_PATH:-/config/letterboxd_diary.csv}
      - DEDUPE_DAYS=${DEDUPE_DAYS:-2}
      - MIN_PERCENT=${MIN_PERCENT:-85}

      # Trakt integration
      - TRAKT_CLIENT_ID=${TRAKT_CLIENT_ID}
      - TRAKT_CLIENT_SECRET=${TRAKT_CLIENT_SECRET}
      - TRAKT_ACCESS_TOKEN=${TRAKT_ACCESS_TOKEN}
      - TRAKT_REDIRECT_URI=${TRAKT_REDIRECT_URI}
      - ENABLE_TRAKT_SYNC=${ENABLE_TRAKT_SYNC:-true}

      # IMDb integration
      - IMDB_RATINGS_CSV=${IMDB_RATINGS_CSV:-/config/imdb/ratings.csv}
      - IMDB_WATCHLIST_CSV=${IMDB_WATCHLIST_CSV:-/config/imdb/watchlist.csv}
      - ENABLE_WATCHLIST_SYNC=${ENABLE_WATCHLIST_SYNC:-true}
      - ENABLE_COLLECTION_SYNC=${ENABLE_COLLECTION_SYNC:-true}

      # Optional webhook notifications
      - WEBHOOK_URL=${WEBHOOK_URL:-}

    volumes:
      - ./data:/config
    ports:
      - "8089:8089"
    command: >
      bash -c "
        echo 'Starting Plexboxd sync service...';
        python -m src.main
      "
```
## ⚙️ Setup Guide

### 1️⃣ Plex Setup

1. Get your **Plex Token**:
   - Open Plex Web → Settings → Account → Show Advanced → Token
   - Copy the long token string.

2. Set your **Plex Base URL**:
   - Usually `http://<your-server-ip>:32400`

3. Confirm your libraries are correctly matched to **The Movie Database (TMDb)** and/or **IMDb** so IDs are available.

---

### 2️⃣ Letterboxd Setup

Letterboxd does not currently have a full public write API,  
so Plexboxd uses CSV-based sync for diary entries.

1. In your `.env`, set:

```
CSV_PATH=/config/letterboxd_diary.csv
```

2. This CSV file will be automatically filled with watched items that can be imported to Letterboxd.

3. Import manually:
   - Visit https://letterboxd.com/import/
   - Upload the generated CSV to sync your diary entries.

---

### 3️⃣ Trakt.tv Setup

1. Create a new Trakt app:  
   https://trakt.tv/oauth/applications

2. Copy your credentials:
   - Client ID  
   - Client Secret  
   - Access Token (after manual auth)

3. Add them to `.env`:

```
TRAKT_CLIENT_ID=your_trakt_client_id
TRAKT_CLIENT_SECRET=your_trakt_client_secret
TRAKT_ACCESS_TOKEN=your_trakt_access_token
```

Once configured, Plexboxd can:
- Add IMDb movies to your Trakt watchlist  
- Create or update Trakt lists from Plex collections  
- Sync watched items from Plex to Trakt  

---

### 4️⃣ IMDb Setup

1. Export your ratings and watchlist from IMDb:
   - Visit https://www.imdb.com/list/ratings → **Export**
   - Visit https://www.imdb.com/list/watchlist → **Export**

2. Place them in your config volume (e.g. `/config/imdb/`).

3. Add to `.env`:

```
IMDB_RATINGS_CSV=/config/imdb/ratings.csv
IMDB_WATCHLIST_CSV=/config/imdb/watchlist.csv
```

4. Run manual syncs:

```
# IMDb Watchlist → Trakt
docker exec -it plexboxd python -c "from src.sync_jobs import sync_imdb_watchlist_to_trakt; import os; print(sync_imdb_watchlist_to_trakt(os.getenv('IMDB_WATCHLIST_CSV')))"
```

---


## 5️⃣ Tautulli setup
- **Notifier:** Webhook
- **URL:** `http://YOUR_SERVER:8089/webhook/tautulli`
- **Header (optional):** `X-Webhook-Secret: <WEBHOOK_SECRET>`
- **Trigger:** Playback Stopped
- **Payload (JSON example):**
```json
{
  "event": "{event}",
  "media_type": "{media_type}",
  "title": "{title}",
  "year": "{year}",
  "imdb_id": "{imdb_id}",
  "tmdb_id": "{themoviedb_id}",
  "user": "{username}",
  "user_rating": "{user_rating}",
  "percent_complete": "{percent_complete}",
  "stopped": "{stopped}"
}
```
Service will listen on `http://0.0.0.0:${PORT}/webhook/tautulli` (default `8089`).

## License
MIT © 2025 nate872711
