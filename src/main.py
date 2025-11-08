#!/usr/bin/env python3
import time, logging
from config_loader import load_config, generate_config_from_env
from src.integrations.sync_engine import run_sync_cycle
from src.integrations.trakt import refresh_trakt_token
def setup_logging(level): logging.basicConfig(level=level.upper() if isinstance(level,str) else "INFO", format="[%(asctime)s] [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
def main():
    try: config = load_config()
    except Exception: generate_config_from_env(); config = load_config()
    setup_logging(config["server"].get("log_level","INFO"))
    logging.info("WatchWeave starting…")
    try: config = refresh_trakt_token(config)
    except Exception as e: logging.warning("Trakt refresh skipped: %s", e)
    while True:
        try:
            summary = run_sync_cycle(config)
            logging.info("Summary: %s", summary)
        except KeyboardInterrupt: break
        except Exception as e: logging.exception("Cycle error: %s", e); time.sleep(30)
        time.sleep(config["sync"]["interval_minutes"]*60)
if __name__ == "__main__": main()
