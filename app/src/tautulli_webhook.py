from flask import Blueprint, request, jsonify, abort
from .config import get_settings
from .utils import (append_row, recently_logged, lb_rating_from_10,
                    lb_uri, iso_to_ymd)
from .letterboxd_csv import DiaryRow

bp = Blueprint("tautulli", __name__)
settings = get_settings()

@bp.post("/webhook/tautulli")
def receive():
    # Optional shared secret header
    secret = settings.webhook_secret
    if secret and request.headers.get("X-Webhook-Secret") != secret:
        abort(401)

    payload = request.get_json(silent=True) or {}
    event = (payload.get("event") or "").lower()
    media_type = (payload.get("media_type") or "").lower()

    if event != "playback_stopped":
        return jsonify({"ok": True, "skipped": "not playback_stopped"}), 200
    if media_type not in ("movie", "video"):
        return jsonify({"ok": True, "skipped": "not a movie"}), 200

    percent = float(payload.get("percent_complete") or payload.get("progress") or 0)
    if percent < settings.min_percent:
        return jsonify({"ok": True, "skipped": f"percent {percent} < {settings.min_percent}"}), 200

    title = payload.get("title") or payload.get("full_title") or "Unknown"
    year = payload.get("year")
    imdb_id = payload.get("imdb_id")
    tmdb_id = (str(payload.get("tmdb_id")).strip() if payload.get("tmdb_id") else None)

    rating10 = None
    try:
        rating10 = float(payload.get("user_rating")) if payload.get("user_rating") is not None else None
    except Exception:
        rating10 = None

    rating = lb_rating_from_10(rating10)
    uri = lb_uri(imdb_id, tmdb_id)
    date_ymd = iso_to_ymd(payload.get("stopped"))

    # Dedup
    if recently_logged(settings.csv_path, title, year, settings.dedupe_days):
        return jsonify({"ok": True, "skipped": "dedupe window"}), 200

    # Rewatch detection: if the same title+year appears earlier in CSV
    rewatch = ""
    try:
        with open(settings.csv_path, encoding="utf-8") as f:
            import csv
            for row in csv.DictReader(f):
                if row.get("Name") == title and (row.get("Year") or "") == (str(year) if year else ""):
                    rewatch = "Yes"; break
    except FileNotFoundError:
        pass

    row = DiaryRow(
        Date=date_ymd,
        Name=title,
        Year=int(year) if str(year).isdigit() else None,
        Letterboxd_URI=uri,
        Rating=rating,
        Rewatch=rewatch,
    )
    append_row(settings.csv_path, row)

    return jsonify({"ok": True, "logged": row.as_csv_row()}), 200
