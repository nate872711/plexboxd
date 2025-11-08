import csv, os
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class IMDbItem:
    title: str
    year: Optional[int]
    imdb_id: Optional[str]
    rating: Optional[float] = None
    type: str = "movie"

def load_imdb_csv(path: str) -> List[IMDbItem]:
    items: List[IMDbItem] = []
    if not path or not os.path.exists(path):
        return items
    with open(path, newline="", encoding="utf-8") as f:
        rdr = csv.DictReader(f)
        for row in rdr:
            imdb_id = row.get("Const") or row.get("imdbID") or ""
            t = row.get("Title") or ""
            y = row.get("Year") or row.get("Release Year") or ""
            r = row.get("Your Rating") or row.get("Rating") or ""
            try:
                y_i = int(y) if str(y).isdigit() else None
            except Exception:
                y_i = None
            try:
                r_f = float(r) if r else None
            except Exception:
                r_f = None
            items.append(IMDbItem(title=t, year=y_i, imdb_id=imdb_id if imdb_id else None, rating=r_f))
    return items
