#!/usr/bin/env python3
"""
WatchWeave — Media Sync Service
--------------------------------
Synchronizes watched history, lists, and ratings between Plex, Trakt,
Letterboxd, and IMDb. This version supports both Docker env configuration
and config.yml auto-generation.
"""

import os
import time
import yaml
import logging
import requests
from datetime import datetime, timedelta

CONFIG_PATH = "/config/config.yml"


# =====================================================
# CONFIG HANDLING
# =====================================================

def generate_config_from_env():
    """Generate /config/config.yml from environment variables if it doesn't exist."""
    os.makedirs("/config", exist_ok=True)
    config = {
        "server": {
            "timezone": os.getenv("TZ", "UTC"),
            "log_level": os.getenv("LOG_LEVEL", "INFO"),
        },
        "plex": {
            "enabled": os.getenv("PLEX_ENABLED", "false").lower() == "true",
            "server_url": os.getenv("PLEX_SERVER_URL"),
            "token": os.getenv("PLEX_TOKEN"),
            "username": os.getenv("PLEX_USERNAME"),
        },
        "letterboxd": {
            "enabled": os.getenv("LETTERBOXD_ENABLED", "false").lower() == "true",
            "username": os.getenv("LETTERBOXD_USERNAME"),
            "password": os.getenv("LETTERBOXD_PASSWORD"),
        },
        "trakt": {
            "enabled": os.getenv("TRAKT_ENABLED", "false").lower() == "true",
            "client_id": os.getenv("TRAKT_CLIENT_ID"),
            "client_secret": os.getenv("TRAKT_CLIENT_SECRET"),
            "access_token": os.getenv("TRAKT_ACCESS_TOKEN"),
            "refresh_token": os.getenv("TRAKT_REFRESH_TOKEN"),
            "last_refreshed": datetime.utcnow().isoformat(),
        },
        "imdb": {
            "enabled": os.getenv("IMDB_ENABLED", "false").lower() == "true",
            "import_csv_path": os.getenv("IMDB_CSV_PATH"),
        },
        "sync": {
            "interval_minutes": int(os.getenv("SYNC_INTERVAL_MINUTES", "30")),
            "direction": os.getenv("SYNC_DIRECTION", "plex->trakt,letterboxd,imdb"),
        },
    }

    with open(CONFIG_PATH, "w") as f:
        yaml.dump(config, f)

    logging.info("✅ Config generated from environment variables.")


def load_config():
    """Load existing config or generate one if missing."""
    if not os.path.exists(CONFIG_PATH):
        generate_config_from_env()
    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)


def save_config(config):
    """Save the config back to file after token refresh."""
    with open(CONFIG_PATH, "w") as f:
        yaml.dump(config, f, sort_keys=False)


# =====================================================
# TRAKT TOKEN REFRESH
# =====================================================

def refresh_trakt_token(config):
    """Automatically refresh Trakt access token if possible."""
    trakt = config.get("trakt", {})
    if not trakt.get("enabled") or not trakt.get("refresh_token"):
        return config  # Nothing to refresh

    logging.info("🔄 Checking Trakt token validity...")

    try:
        url = "https://api.trakt.tv/oauth/token"
        payload = {
            "refresh_token": trakt["refresh_token"],
            "client_id": trakt["client_id"],
            "client_secret": trakt["client_secret"],
            "redirect_uri": "urn:ietf:wg:oauth:2.0:oob",
            "grant_type": "refresh_token",
        }
        res = requests.post(url, json=payload, timeout=10)
        if res.status_code == 200:
            new_data = res.json()
            trakt["access_token"] = new_data["access_token"]
            trakt["refresh_token"] = new_data.get("refresh_token", trakt["refresh_token"])
            trakt["last_refreshed"] = datetime.utcnow().isoformat()
            save_config(config)
            logging.info("✅ Trakt token refreshed successfully.")
        else:
            logging.warning(f"⚠️ Trakt token refresh failed ({res.status_code}): {res.text}")
    except Exception as e:
        logging.error(f"❌ Error refreshing Trakt token: {e}")

    return config


# =====================================================
# SYNC PLACEHOLDERS
# =====================================================

def sync_plex_to_trakt(config):
    logging.info("🔁 Syncing Plex → Trakt (placeholder)...")
    # TODO: Implement real sync logic
    time.sleep(1)


def sync_trakt_to_letterboxd(config):
    logging.info("🔁 Syncing Trakt → Letterboxd (placeholder)...")
    # TODO: Implement real sync logic
    time.sleep(1)


def sync_imdb_to_trakt(config):
    logging.info("🔁 Syncing IMDb → Trakt (placeholder)...")
    # TODO: Implement real sync logic
    time.sleep(1)


# =====================================================
# MAIN LOOP
# =====================================================

def main():
    config = load_config()

    # Setup logging
    logging.basicConfig(
        level=config["server"].get("log_level", "INFO"),
        format="[%(asctime)s] [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    logging.info("🚀 WatchWeave starting up...")
    logging.info(f"🕒 Sync interval: {config['sync']['interval_minutes']} minutes")

    # Refresh Trakt token once at startup
    config = refresh_trakt_token(config)

    while True:
        try:
            logging.info("🔄 Beginning sync cycle...")
            if config["plex"]["enabled"] and config["trakt"]["enabled"]:
                sync_plex_to_trakt(config)

            if config["trakt"]["enabled"] and config["letterboxd"]["enabled"]:
                sync_trakt_to_letterboxd(config)

            if config["imdb"]["enabled"] and config["trakt"]["enabled"]:
                sync_imdb_to_trakt(config)

            logging.info("✅ Sync cycle complete. Sleeping...")
            time.sleep(config["sync"]["interval_minutes"] * 60)
        except KeyboardInterrupt:
            logging.info("🛑 WatchWeave stopped manually.")
            break
        except Exception as e:
            logging.error(f"❌ Error during sync cycle: {e}")
            time.sleep(30)  # retry after 30s if crash


if __name__ == "__main__":
    main()
