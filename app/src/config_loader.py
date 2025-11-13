import os
import yaml
import logging
from pathlib import Path

log = logging.getLogger("config")

CONFIG_PATH = Path("/config/config.yml")


def _env_bool(name: str, default: bool = False) -> bool:
    val = os.getenv(name)
    if val is None:
        return default
    return str(val).strip().lower() in ("1", "true", "yes", "on")


def _env_int(name: str, default: int) -> int:
    val = os.getenv(name)
    if val is None:
        return default
    try:
        return int(val)
    except ValueError:
        return default


def generate_config_from_env() -> dict:
    """Builds an in-memory config structure from environment variables."""
    config = {
        "general": {
            "log_level": os.getenv("LOG_LEVEL", "INFO"),
            "sync_interval_minutes": _env_int("SYNC_INTERVAL_MINUTES", 30),
            "sync_direction": os.getenv(
                "SYNC_DIRECTION",
                "plex->trakt,letterboxd,imdb",
            ),
        },
        "plex": {
            "enabled": _env_bool("PLEX_ENABLED", True),
            "server_url": os.getenv("PLEX_SERVER_URL", "").strip(),
            "token": os.getenv("PLEX_TOKEN", "").strip(),
            "username": os.getenv("PLEX_USERNAME", "").strip(),
        },
        "tautulli": {
            "enabled": _env_bool("TAUTULLI_ENABLED", False),
            "api_url": os.getenv("TAUTULLI_API_URL", "").strip(),
            "api_key": os.getenv("TAUTULLI_API_KEY", "").strip(),
        },
        "trakt": {
            "enabled": _env_bool("TRAKT_ENABLED", False),
            "client_id": os.getenv("TRAKT_CLIENT_ID", "").strip(),
            "client_secret": os.getenv("TRAKT_CLIENT_SECRET", "").strip(),
            "access_token": os.getenv("TRAKT_ACCESS_TOKEN", "").strip(),
            "refresh_token": os.getenv("TRAKT_REFRESH_TOKEN", "").strip(),
        },
        "letterboxd": {
            "enabled": _env_bool("LETTERBOXD_ENABLED", False),
            "username": os.getenv("LETTERBOXD_USERNAME", "").strip(),
            "password": os.getenv("LETTERBOXD_PASSWORD", "").strip(),
            # if true, we only log what would be sent; no real diary writes
            "dry_run": _env_bool("LETTERBOXD_DRY_RUN", False),
        },
        "imdb": {
            "enabled": _env_bool("IMDB_ENABLED", False),
            "csv_path": os.getenv("IMDB_CSV_PATH", "/config/imdb_ratings.csv").strip(),
        },
        "tvdb": {
            "enabled": _env_bool("TVDB_ENABLED", False),
            "api_key": os.getenv("TVDB_API_KEY", "").strip(),
            "pin": os.getenv("TVDB_PIN", "").strip(),
        },
        "serializd": {
            "enabled": _env_bool("SERIALIZD_ENABLED", False),
            "api_key": os.getenv("SERIALIZD_API_KEY", "").strip(),
        },
        "musicboard": {
            "enabled": _env_bool("MUSICBOARD_ENABLED", False),
            "username": os.getenv("MUSICBOARD_USERNAME", "").strip(),
            "api_key": os.getenv("MUSICBOARD_API_KEY", "").strip(),
        },
        "tmdb": {
            "enabled": _env_bool("TMDB_ENABLED", False),
            "api_key": os.getenv("TMDB_API_KEY", "").strip(),
        },
        "custom_lists": {
            "enabled": _env_bool("CUSTOM_LISTS_ENABLED", False),
        },
    }

    return config


def load_config() -> dict:
    """
    Loads /config/config.yml if it exists; otherwise generates it from env vars
    and writes it out for the user to inspect/edit.
    """
    if CONFIG_PATH.exists():
        try:
            with CONFIG_PATH.open("r", encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
            log.info("Loaded config from %s", CONFIG_PATH)
            return data
        except Exception as e:
            log.error("Failed to read config.yml (%s), regenerating from env.", e)

    # Generate fresh config from env
    config = generate_config_from_env()

    try:
        CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with CONFIG_PATH.open("w", encoding="utf-8") as f:
            yaml.safe_dump(config, f, sort_keys=False)
        log.info("⚠️ config.yml not found — generated from environment variables")
    except Exception as e:
        log.error("Failed to write config.yml: %s", e)

    return config
