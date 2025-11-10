# <img src="nate872711/watchweave/branding/watchweave-icon.png" width="20"> WatchWeave


<img src="nate872711/watchweave/branding/watchweave-banner.png" width="500">





[![Docker Pulls](https://img.shields.io/docker/pulls/nate8727/watchweave?logo=docker&style=flat-square)](https://hub.docker.com/r/nate8727/watchweave)
[![GitHub Release](https://img.shields.io/github/v/release/nate872711/watchweave?logo=github&style=flat-square)](https://github.com/nate872711/watchweave/releases)
[![Build & Release](https://github.com/nate872711/watchweave/actions/workflows/release.yml/badge.svg)](https://github.com/nate872711/watchweave/actions/workflows/release.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)


**Your Plex movies, your Letterboxd diary — finally in sync.**

**WatchWeave** is a self-hosted integration bridge between **Plex**, **Letterboxd**, **Trakt**, and **IMDb**.  

It syncs your watched movies and shows, updates your Letterboxd diary, manages watchlists and collections, and provides export/import utilities for your media ecosystem.

***WatchWeave is currently in beta***

---

## 🚀 Features

- 🔄 **Automatic synchronization** between Plex, Trakt, Letterboxd, IMDb, and more
- 🧠 Smart merging of watch history, ratings, lists, and collections
- 🏗 **Auto-generates `config.yml`** dynamically from Docker environment variables --- no manual setup required
- 🕒 Configurable sync intervals and direction (e.g., Plex → Trakt, or bidirectional)
- 🐳 Fully Dockerized with minimal configuration
- 🔐 Secure token handling and optional OAuth2-based login system
- 🧩 Modular design --- ready for plugin-based expansions and future integrations
- 📈 **Web dashboard (planned)** on port **8089** for real-time sync logs, manual triggers, and system overview<br>  → Currently reserved; dashboard service will be enabled in an upcoming release
- 🧾 Detailed logs saved to `/logs` for tracking and diagnostics
- 🧰 Cross-platform support for Linux, macOS, and Windows

---

## 🧱 Requirements

- Docker & Docker Compose  
- Plex server with valid API token  
- (Optional) Trakt, Letterboxd, and/or IMDb accounts  
- (Optional) Tautulli instance with API key  

---

## 🛣️ Roadmap

- [x] Git Tag Releases (e.g.,`v.1.0.1`, `v1.2.0`)
- [x] TV Libraries + TheTVDB + Serializd
- [x] Music Libraries + Musicboard
- [x] TMDb Integration
- [x] Custom Lists Support
- [ ] Web UI / Dashboard
- [ ] Smart Retry + Failure Queue System
- [ ] Bidirectional + Incremental Sync
- [ ] Token Refresh for All Services
- [ ] Plugin Framework
- [ ] Rest API/SDK
- [ ] Multi-User Support
- [ ] See [ROADMAP.md](ROADMAP.md) for Complete List

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
      ##############################################################
      # 🔧 GENERAL SETTINGS
      ##############################################################
      TZ: Etc/UTC
      LOG_LEVEL: INFO
      SYNC_INTERVAL_MINUTES: 30
      SYNC_DIRECTION: "plex->trakt,letterboxd,imdb"

      ##############################################################
      # 🎬 PLEX
      ##############################################################
      PLEX_ENABLED: true
      PLEX_SERVER_URL: "http://plex.local:32400"
      PLEX_TOKEN: ""
      PLEX_USERNAME: ""

      ##############################################################
      # 📈 TAUTULLI (OPTIONAL)
      ##############################################################
      TAUTULLI_ENABLED: false
      TAUTULLI_API_URL: ""
      TAUTULLI_API_KEY: ""

      ##############################################################
      # 🎞 TRAKT
      ##############################################################
      TRAKT_ENABLED: true
      TRAKT_CLIENT_ID: ""
      TRAKT_CLIENT_SECRET: ""
      TRAKT_ACCESS_TOKEN: ""
      TRAKT_REFRESH_TOKEN: ""

      ##############################################################
      # 🎬 LETTERBOXD (OPTIONAL)
      ##############################################################
      LETTERBOXD_ENABLED: false
      LETTERBOXD_USERNAME: ""
      LETTERBOXD_PASSWORD: ""

      ##############################################################
      # 🎥 IMDb (OPTIONAL)
      ##############################################################
      IMDB_ENABLED: false
      IMDB_CSV_PATH: "/config/imdb_ratings.csv"

      ##############################################################
      # 📺 TheTVDB (OPTIONAL)
      ##############################################################
      TVDB_ENABLED: false
      TVDB_API_KEY: ""
      TVDB_PIN: ""

      ##############################################################
      # 🎞 SERIALIZD (OPTIONAL)
      ##############################################################
      SERIALIZD_ENABLED: false
      SERIALIZD_API_KEY: ""

      ##############################################################
      # 🎵 MUSICBOARD (OPTIONAL)
      ##############################################################
      MUSICBOARD_ENABLED: false
      MUSICBOARD_USERNAME: ""
      MUSICBOARD_API_KEY: ""

      ##############################################################
      # 🎬 TMDb (OPTIONAL)
      ##############################################################
      TMDB_ENABLED: false
      TMDB_API_KEY: ""

      ##############################################################
      # 🗂 CUSTOM LISTS → PLEX COLLECTIONS (OPTIONAL)
      ##############################################################
      CUSTOM_LISTS_ENABLED: false

    volumes:
      - ./config:/config
      - ./logs:/logs

    # Optional: attach to a shared Docker network with Plex/Tautulli
    # networks:
    #   - plexnet

# Optional shared network for media apps
# networks:
#   plexnet:
#     driver: bridge

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

### <img src="app/src/assets/plex-icon.png" width="20"> Plex
1. [Sign in to your Plex account](https://support.plex.tv/articles/200933616-plex-account/) in Plex Web App  
2. Browse to a library item and [view the XML](https://support.plex.tv/articles/201998867-investigate-media-information-and-formats/) for it
3. Look in the URL and find the token as the `X-Plex-Token` value
4. Paste the token into the docker-compose.yml

   ```bash
   PLEX_ENABLED=true
   PLEX_SERVER_URL=http://your-plex-ip:32400
   PLEX_TOKEN=your-plex-token
   ```

> 💡 Tip: WatchWeave works fine even without Tautulli — it just uses Plex history directly.


---

### <img src="app/src/assets/tautulli-icon.png" width="20"> Tautulli (Optional)
1. Open your Tautulli web interface → Settings → Web Interface → API Key  
2. Copy your key and URL:
   ```bash
   TAUTULLI_ENABLED=true
   TAUTULLI_API_URL=http://your-tautulli:8181/api/v2
   TAUTULLI_API_KEY=your-api-key
   ```

---

### <img src="app/src/assets/Trakt.tv-icon.png" width="20"> Trakt.tv
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

### <img src="app/src/assets/letterboxd-icon.png" width="20"> Letterboxd
1. Supply your **username** and **password** for watchlist and list syncing:
   ```bash
   LETTERBOXD_ENABLED=true
   LETTERBOXD_USERNAME=your-username
   LETTERBOXD_PASSWORD=your-password
   ```

---

### <img src="app/src/assets/imdb-icon.png" width="20"> IMDb
1. Visit your IMDb ratings page and click **Export**.  
2. Save the CSV as `imdb_ratings.csv` in your `/config` folder.  
3. Set:
   ```bash
   IMDB_ENABLED=true
   IMDB_CSV_PATH=/config/imdb_ratings.csv
   ```
   
---

### <img src="app/src/assets/TheTVDB-icon.png" width="20"> TheTVDB
1. Create an API key and user PIN from your [TheTVDB account settings](https://thetvdb.com/dashboard/account).
2. Enable in Docker Compose:
   ```
   TVDB_ENABLED: true
   TVDB_API_KEY: "your-key"
   TVDB_PIN: "your-pin"
   ```
3. Used to enhance TV metadata and episode matching.
   

---

### <img src="app/src/assets/serializd-icon.png" width="20"> Serializd
1. Get your API key from your [Serializd account](https://serializd.com/).
2. Enable it:
   ```
   SERIALIZD_ENABLED: true
   SERIALIZD_API_KEY: "your-api-key"
   ```

---

### <img src="app/src/assets/musicboard-icon.png" width="20"> Musicboard
1. Obtain your Musicboard API key and username.
2. Enable in Docker Compose:
   ```
   MUSICBOARD_ENABLED: true
   MUSICBOARD_USERNAME: "your-username"
   MUSICBOARD_API_KEY: "your-key"
   ```
3. Adds syncing support for your Plex Music library (albums, artists, reviews)


---

### <img src="app/src/assets/TMDb-icon.png" width="20"> TMDb
1. Get your TMDb API key from [https://www.themoviedb.org/settings/api](https://www.themoviedb.org/settings/api).
2. Enable in Docker Compose:
   ```
   TMDB_ENABLED: true
   TMDB_API_KEY: "your-tmdb-api-key"
   ```
   3. Used as a fallback for metadata (genre, posters, overview)

---

### 🗂 Custom Lists
1. Enable to auto-create **Plex Smart Collections** based on  your Trakt, Letterboxd, or Serializd lists:
   ```
   CUSTOM_LISTS_ENABLED: true
   ```

---

### 🧠 Logging & Status

All logs are written to /logs inside your container.
Each sync cycle outputs a summary:
```
📊 Summary: {'plex->trakt_updated': 3, 'plex_count': 124, 'trakt_count': 117, 'imdb_ratings': 
```


MIT © 2025 nate872711
