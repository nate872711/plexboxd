import os, csv
from datetime import datetime, timedelta
from dateutil import parser as dtparse
from .letterboxd_csv import HEADERS, DiaryRow

def ensure_csv(path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if not os.path.exists(path):
        with open(path, "w", newline="", encoding="utf-8") as f:
            csv.DictWriter(f, fieldnames=HEADERS).writeheader()

def append_row(path: str, row: DiaryRow) -> None:
    ensure_csv(path)
    with open(path, "a", newline="", encoding="utf-8") as f:
        csv.DictWriter(f, fieldnames=HEADERS).writerow(row.as_csv_row())

def recently_logged(path: str, title: str, year: str | int | None, dedupe_days: int) -> bool:
    if not os.path.exists(path):
        return False
    cutoff = datetime.utcnow() - timedelta(days=dedupe_days)
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row.get("Name") == title and (row.get("Year") or "") == (str(year) if year else ""):
                try:
                    d = dtparse.parse(row.get("Date")).replace(tzinfo=None)
                    if d >= cutoff:
                        return True
                except Exception:
                    pass
    return False

def lb_rating_from_10(r10: float | None) -> str | None:
    if r10 is None:
        return None
    stars = max(0.5, min(5.0, round((r10 / 2.0) * 2) / 2))
    return str(int(stars)) if float(stars).is_integer() else f"{stars:.1f}"

def lb_uri(imdb_id: str | None, tmdb_id: str | None) -> str | None:
    if imdb_id:
        imdb_id = imdb_id.strip()
        if not imdb_id.startswith("tt"):
            imdb_id = "tt" + imdb_id
        return f"https://letterboxd.com/imdb/{imdb_id}/"
    if tmdb_id:
        return f"https://www.themoviedb.org/movie/{tmdb_id}"
    return None

def iso_to_ymd(iso_str: str | None) -> str:
    if not iso_str:
        return datetime.utcnow().strftime("%Y-%m-%d")
    try:
        if iso_str.isdigit():
            return datetime.utcfromtimestamp(int(iso_str)).strftime("%Y-%m-%d")
    except Exception:
        pass
    try:
        return dtparse.isoparse(iso_str).date().strftime("%Y-%m-%d")
    except Exception:
        return datetime.utcnow().strftime("%Y-%m-%d")
