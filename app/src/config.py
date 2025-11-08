import os
from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    port: int = int(os.getenv("PORT", "8089"))
    webhook_secret: str | None = os.getenv("WEBHOOK_SECRET")
    csv_path: str = os.getenv("CSV_PATH", "/data/letterboxd_diary_queue.csv")
    dedupe_days: int = int(os.getenv("DEDUPE_DAYS", "2"))
    min_percent: float = float(os.getenv("MIN_PERCENT", "85"))

def get_settings() -> Settings:
    return Settings()
