# <img src="/branding/watchweave-icon.png" width="20"> WatchWeave


<img src="/branding/watchweave-banner.png" width="500">





[![Docker Pulls](https://img.shields.io/docker/pulls/nate8727/watchweave?logo=docker&style=flat-square)](https://hub.docker.com/r/nate8727/watchweave)
[![GitHub Release](https://img.shields.io/github/v/release/nate872711/watchweave?logo=github&style=flat-square)](https://github.com/nate872711/watchweave/releases)
[![Build & Release](https://github.com/nate872711/watchweave/actions/workflows/release.yml/badge.svg)](https://github.com/nate872711/watchweave/actions/workflows/release.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)


**Your Plex movies, your Letterboxd diary — finally in sync.**

**WatchWeave** is a self-hosted integration bridge between **Plex**, **Letterboxd**, **Trakt**, and **IMDb**.  
It syncs your watched movies and shows, updates your Letterboxd diary, manages watchlists and collections, and provides export/import utilities for your media ecosystem.

---

## 🚀 Features

- ✅ Sync **watched status** across Plex, Trakt, and Letterboxd  
- ✅ Import **IMDb ratings** directly from your exported CSV  
- ✅ Optional **Tautulli** integration for richer playback data  
- ✅ Auto-generates `/config/config.yml` from environment variables  
- ✅ Graceful fallback to Plex-only mode if Tautulli unavailable  
- ✅ Built-in Trakt token refresh  
- ✅ Clear sync summaries in logs after every cycle  

---

## 🧱 Requirements

- Docker & Docker Compose  
- Plex server with valid API token  
- (Optional) Trakt, Letterboxd, and/or IMDb accounts  
- (Optional) Tautulli instance with API key  

---

## 🛣️ Roadmap

- [ ] Local webui dashboard with sync stats  
- [ ] Smart retry + failure queue system  

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

### Clone the Repository
```bash
git clone https://github.com/nate872711/watchweave.git
cd watchweave
```
### Example docker compose
```yaml
services:
  watchweave:
    image: nate8727/watchweave:latest
    container_name: watchweave
    restart: unless-stopped
    ports:
      - "8089:8089"

    environment:
      # 🌍 General
      - TZ=Etc/UTC
      - LOG_LEVEL=INFO

      # 🎬 Plex
      - PLEX_ENABLED=true
      - PLEX_SERVER_URL=http://plex.local:32400
      - PLEX_TOKEN=YOUR_PLEX_TOKEN
      - PLEX_USERNAME=YOUR_PLEX_USERNAME

      # 📈 Tautulli
      - TAUTULLI_ENABLED=true
      - TAUTULLI_API_URL=http://tautulli.local:8181/api/v2
      - TAUTULLI_API_KEY=YOUR_TAUTULLI_API_KEY

      # 🎞️ Trakt
      - TRAKT_ENABLED=true
      - TRAKT_CLIENT_ID=YOUR_TRAKT_CLIENT_ID
      - TRAKT_CLIENT_SECRET=YOUR_TRAKT_CLIENT_SECRET
      - TRAKT_ACCESS_TOKEN=YOUR_TRAKT_ACCESS_TOKEN
      - TRAKT_REFRESH_TOKEN=YOUR_TRAKT_REFRESH_TOKEN

      # 🎥 Letterboxd
      - LETTERBOXD_ENABLED=true
      - LETTERBOXD_USERNAME=YOUR_LETTERBOXD_USERNAME
      - LETTERBOXD_PASSWORD=YOUR_LETTERBOXD_PASSWORD

      # 🎬 IMDb
      - IMDB_ENABLED=true
      - IMDB_CSV_PATH=/config/imdb_ratings.csv

      # 🔄 Sync
      - SYNC_INTERVAL_MINUTES=30
      - SYNC_DIRECTION=plex->trakt,letterboxd,imdb

    volumes:
      - ./config:/config
      - ./logs:/logs

    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8089/health || exit 1"]
      interval: 60s
      timeout: 10s
      retries: 3
      start_period: 20s
```
---

## ⚙️ Environment Variables

| Variable | Description |
|-----------|-------------|
| `TZ` | Timezone, e.g. `America/New_York` |
| `LOG_LEVEL` | Logging verbosity (`INFO`, `DEBUG`, etc.) |
| `SYNC_INTERVAL_MINUTES` | How often to run syncs |
| `SYNC_DIRECTION` | Comma-separated directions (e.g. `plex->trakt,letterboxd`) |

---

## ⚙️ Setup Guide

### 🎬 Plex
1. [Sign in to your Plex account](https://support.plex.tv/articles/200933616-plex-account/) in Plex Web App  
2. Browse to a library item and [view the XML](https://support.plex.tv/articles/201998867-investigate-media-information-and-formats/) for it
3. Look in the URL and find the token as the **X-Plex-Token** value
4. Paste the token into the docker-compose.yml

   ```bash
   PLEX_ENABLED=true
   PLEX_SERVER_URL=http://your-plex-ip:32400
   PLEX_TOKEN=your-plex-token
   ```

> 💡 Tip: WatchWeave works fine even without Tautulli — it just uses Plex history directly.


---

### 📈 Tautulli (Optional)
1. Open your Tautulli web interface → Settings → Web Interface → API Key  
2. Copy your key and URL:
   ```bash
   TAUTULLI_ENABLED=true
   TAUTULLI_API_URL=http://your-tautulli:8181/api/v2
   TAUTULLI_API_KEY=your-api-key
   ```

---

### 🎥 Letterboxd
1. Supply your **username** and **password** for watchlist and list syncing:
   ```bash
   LETTERBOXD_ENABLED=true
   LETTERBOXD_USERNAME=your-username
   LETTERBOXD_PASSWORD=your-password
   ```

---

### 🎞️ Trakt.tv
1. Go to [https://trakt.tv/oauth/applications](https://trakt.tv/oauth/applications)  
2. Create a new application using:
   - **Redirect URI:** `urn:ietf:wg:oauth:2.0:oob`  
3. Copy your **Client ID** and **Client Secret**  
4. Generate tokens:
   ```bash
   curl -X POST https://api.trakt.tv/oauth/token \
     -d '{"code":"AUTH_CODE","client_id":"CLIENT_ID","client_secret":"CLIENT_SECRET","redirect_uri":"urn:ietf:wg:oauth:2.0:oob","grant_type":"authorization_code"}'
   ```
5. Add them to your docker environment:
   ```bash
   TRAKT_ENABLED=true
   TRAKT_CLIENT_ID=your-client-id
   TRAKT_CLIENT_SECRET=your-client-secret
   TRAKT_ACCESS_TOKEN=your-access-token
   TRAKT_REFRESH_TOKEN=your-refresh-token
   ```

---

### ⭐ IMDb
1. Visit your IMDb ratings page and click **Export**.  
2. Save the CSV as `imdb_ratings.csv` in your `/config` folder.  
3. Set:
   ```bash
   IMDB_ENABLED=true
   IMDB_CSV_PATH=/config/imdb_ratings.csv
   ```

---


MIT © 2025 nate872711
