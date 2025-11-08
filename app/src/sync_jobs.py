import os
from typing import Dict, List
from .trakt_client import TraktClient
from .imdb_import import load_imdb_csv
from .letterboxd_csv import DiaryRow
from .utils import ensure_csv, lb_uri

def sync_imdb_watchlist_to_trakt(imdb_csv_path: str) -> Dict:
    items = load_imdb_csv(imdb_csv_path)
    imdb_ids = [i.imdb_id for i in items if i.imdb_id]
    if not imdb_ids:
        return {"ok": True, "added": 0}
    t = TraktClient()
    res = t.add_to_watchlist(imdb_ids=imdb_ids)
    return {"ok": True, "added": len(imdb_ids), "trakt": res}

def export_imdb_to_letterboxd_csv(imdb_csv_path: str, out_csv_path: str) -> Dict:
    ensure_csv(out_csv_path)
    items = load_imdb_csv(imdb_csv_path)
    written = 0
    from datetime import datetime
    today = datetime.utcnow().strftime("%Y-%m-%d")
    for it in items:
        row = DiaryRow(Date=today, Name=it.title, Year=it.year, Letterboxd_URI=lb_uri(it.imdb_id, None), Rating=None, Rewatch="")
        from .utils import append_row
        append_row(out_csv_path, row)
        written += 1
    return {"ok": True, "written": written, "out": out_csv_path}

def sync_plex_collections_to_trakt_lists(mapping: Dict[str,str], imdb_ids_by_collection: Dict[str, List[str]]) -> Dict:
    t = TraktClient()
    results = {}
    for coll, slug in mapping.items():
        ids = imdb_ids_by_collection.get(coll, [])
        if not ids:
            results[coll] = {"added": 0}
            continue
        t.create_or_update_list(slug=slug, name=coll, description=f"Plex collection: {coll}", privacy="private")
        res = t.add_movies_to_list(slug=slug, imdb_ids=ids)
        results[coll] = {"added": len(ids), "trakt": res}
    return {"ok": True, "results": results}
