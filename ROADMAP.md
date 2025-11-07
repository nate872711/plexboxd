# 🧭 WatchWeave Roadmap

This document outlines upcoming and potential enhancements planned for **WatchWeave** — a unified media sync service for Plex, Trakt, Letterboxd, IMDb, and more.

---

## 🧩 1. Core Sync & Data Enhancements

### 🔁 Bidirectional Sync
- **Goal:** Allow updates made on Trakt or Letterboxd to sync *back* into Plex.
- **Details:** Compare timestamps (`watched_at`, Plex play date) to resolve direction.
- **Impact:** Enables full two-way synchronization between platforms.

### 🕒 Incremental Sync
- **Goal:** Track last sync timestamp in `/config/state.json` or SQLite.
- **Details:** Only fetch new data since the last successful sync.
- **Impact:** Faster sync cycles and reduced API usage.

### 🎬 Enhanced GUID Matching
- **Goal:** Fallback lookups via TMDb, TheTVDB, or OMDb when IMDb IDs are missing.
- **Impact:** Improves data matching for Plex items with incomplete metadata.

### 🧾 Smart Deduplication
- **Goal:** Cache processed IMDb IDs and Trakt history.
- **Impact:** Avoids redundant calls and unnecessary syncs.

---

## 🌐 2. Integrations Expansion

### 📺 TheTVDB Integration (✅Added in v.1.0.1)
- **Goal:** Improve TV show matching and metadata enrichment.
- **Implementation:** Use [TheTVDB API v4](https://thetvdb.github.io/v4-api/) for series and episode resolution.
- **Impact:** Enhances sync reliability for Plex libraries using TheTVDB agent.

### 🎞️ Serializd Integration (✅Added in v.1.0.1)
- **Goal:** Add support for syncing watched history, ratings, and lists with [Serializd](https://serializd.com/).
- **Implementation:** Use GraphQL API mirroring Trakt's structure.
- **Impact:** Expands WatchWeave’s ecosystem to new social film-tracking users.

### 🎵 Musicboard Integration (✅Added in v.1.0.1)
- **Goal:** Sync Plex music listening activity with [Musicboard](https://musicboard.app/).
- **Implementation:** Match Plex albums and artists, push plays, and sync favorites/reviews.
- **Impact:** Adds support for music collections and listening analytics.

### 📺 TMDb Integration (✅Added in v.1.0.1)
- **Goal:** Pull extra metadata (genre, poster, overview) to improve matching.
- **Impact:** Enriches sync logs and supports deeper integration.

### 🎧 TV & Music Libraries (✅Added in v.1.0.1)
- **Goal:** Extend support to Plex TV shows (`type=2`) and music (`type=10`).
- **Impact:** Broader cross-media coverage.

### 🗂️ Custom Lists Support (✅Added in v.1.0.1)
- **Goal:** Mirror Trakt and Letterboxd lists as Plex Smart Collections.
- **Impact:** Creates synced dynamic playlists in Plex.

---

## ⚙️ 3. Infrastructure & Usability

### 🧠 Web UI / Dashboard
- **Goal:** Create a small UI with connection status, logs, manual sync button, and stats.
- **Tech:** FastAPI + HTMX or React (served on port `8080`).

### 🔄 Manual Sync Endpoint
- **Goal:** Add `/sync` HTTP endpoint to trigger syncs on demand.
- **Impact:** Allows easy automation or manual control.

### 🪣 SQLite Local Cache
- **Goal:** Replace YAML-based cache with SQLite (`/config/data/watchweave.db`).
- **Impact:** Faster and more reliable comparisons.

### 🔐 OAuth Web Flow for Trakt and Serializd
- **Goal:** Simplify login via browser-based authorization.
- **Impact:** Removes need for manual token setup.

---

## 🧰 4. Developer & Power User Features

### 🧪 Dry Run Mode
- **Goal:** Simulate sync without making changes.
- **Impact:** Safer testing and debugging.

### 📜 Webhooks & Notifications
- **Goal:** Send sync summaries to Discord, Slack, or webhooks.
- **Impact:** Keep track of activity remotely.

### 🧠 Token Refresh for All Services
- **Goal:** Extend Trakt auto-refresh to other APIs.
- **Impact:** Completely automated authentication maintenance.

---

## ☁️ 5. Ecosystem & Community

### 🧩 Plugin Framework
- **Goal:** Allow community-contributed integrations via `/src/integrations/custom/`.
- **Impact:** Open ecosystem for new platforms.

### 📦 REST API / SDK
- **Goal:** Offer JSON-based API for external control or dashboard use.
- **Example:**  
  ```bash
  curl -X POST http://localhost:8080/sync --json '{"direction":"plex->trakt"}'
  ```

### 🧾 CLI Tool
- **Goal:** Add a `watchweave` CLI with commands:
  ```
  watchweave sync trakt
  watchweave status
  watchweave token refresh
  ```
- **Impact:** Useful for developers and advanced users.

### 🧭 Multi-User Support
- **Goal:** Allow multiple Plex users linked to separate Trakt or Serializd accounts.
- **Impact:** Great for families or shared servers.

---

## 🧠 6. Advanced / Long-Term Vision

### 🎯 Recommendation Sync
- **Goal:** Sync Trakt, Serializd, and Letterboxd “Recommended” to Plex Collections.
- **Impact:** Personalized discovery inside Plex.

### 📊 Analytics Dashboard
- **Goal:** Visualize viewing trends, genres, and stats via Grafana or Chart.js.
- **Impact:** Adds data insights for power users.

### 🤖 Smart Conflict Resolution
- **Goal:** Use timestamps and heuristics to decide which source wins conflicts.
- **Impact:** Improves accuracy and prevents overwrites.

---

## 🏗️ Contribution Guidelines
If you’d like to contribute:
1. Fork the repo.
2. Create a branch (e.g. `feature/tvdb-integration`).
3. Submit a pull request with a clear description.
4. Include screenshots or logs if applicable.

---

## 📅 Versioning & Planning
Planned for future milestones:
- **v1.1.0:** Add incremental sync + SQLite cache  
- **v1.2.0:** Introduce Web UI dashboard  
- **v1.3.0:** Plugin framework & REST API  


---

**Maintained by:** [@nate872711](https://github.com/nate872711)  
**Docker Hub:** [nate8727/watchweave](https://hub.docker.com/r/nate8727/watchweave)

---
