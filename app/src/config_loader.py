import os, yaml, logging
CONFIG_PATH = "/config/config.yml"
def generate_config_from_env():
    os.makedirs("/config", exist_ok=True)
    def as_bool(name, default=False):
        val = os.getenv(name, str(default)).strip().lower()
        return val in ("1","true","yes","on")
    config = {
        "server":{"timezone":os.getenv("TZ",""),"log_level":os.getenv("LOG_LEVEL","INFO")},
        "plex":{"enabled":as_bool("PLEX_ENABLED"),"server_url":os.getenv("PLEX_SERVER_URL"),"token":os.getenv("PLEX_TOKEN"),"username":os.getenv("PLEX_USERNAME")},
        "tautulli":{"enabled":as_bool("TAUTULLI_ENABLED"),"api_url":os.getenv("TAUTULLI_API_URL"),"api_key":os.getenv("TAUTULLI_API_KEY")},
        "letterboxd":{"enabled":as_bool("LETTERBOXD_ENABLED"),"username":os.getenv("LETTERBOXD_USERNAME"),"password":os.getenv("LETTERBOXD_PASSWORD")},
        "trakt":{"enabled":as_bool("TRAKT_ENABLED"),"client_id":os.getenv("TRAKT_CLIENT_ID"),"client_secret":os.getenv("TRAKT_CLIENT_SECRET"),"access_token":os.getenv("TRAKT_ACCESS_TOKEN"),"refresh_token":os.getenv("TRAKT_REFRESH_TOKEN")},
        "imdb":{"enabled":as_bool("IMDB_ENABLED"),"import_csv_path":os.getenv("IMDB_CSV_PATH")},
        "tvdb":{"enabled":as_bool("TVDB_ENABLED"),"api_key":os.getenv("TVDB_API_KEY"),"pin":os.getenv("TVDB_PIN")},
        "serializd":{"enabled":as_bool("SERIALIZD_ENABLED"),"api_key":os.getenv("SERIALIZD_API_KEY")},
        "musicboard":{"enabled":as_bool("MUSICBOARD_ENABLED"),"username":os.getenv("MUSICBOARD_USERNAME"),"api_key":os.getenv("MUSICBOARD_API_KEY")},
        "tmdb":{"enabled":as_bool("TMDB_ENABLED"),"api_key":os.getenv("TMDB_API_KEY")},
        "custom_lists":{"enabled":as_bool("CUSTOM_LISTS_ENABLED")},
        "sync":{"interval_minutes":int(os.getenv("SYNC_INTERVAL_MINUTES","30")),"direction":os.getenv("SYNC_DIRECTION","plex->trakt,letterboxd,imdb")}
    }
    with open(CONFIG_PATH,"w",encoding="utf-8") as f: yaml.dump(config,f,sort_keys=False,allow_unicode=True)
    logging.info("Config generated from env.")
def load_config():
    if not os.path.exists(CONFIG_PATH): generate_config_from_env()
    with open(CONFIG_PATH,"r",encoding="utf-8") as f: return yaml.safe_load(f)
