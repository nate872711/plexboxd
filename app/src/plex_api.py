import os, requests
from typing import List, Dict

class PlexAPI:
    def __init__(self):
        self.base = os.getenv("PLEX_BASE_URL", "http://localhost:32400").rstrip("/")
        self.token = os.getenv("PLEX_TOKEN")
        if not self.token:
            raise ValueError("PLEX_TOKEN missing")
        self.session = requests.Session()
        self.session.headers.update({"X-Plex-Token": self.token})

    def _url(self, path: str) -> str:
        return f"{self.base}{path}"

    def get_collections(self, library_key: str) -> List[Dict]:
        r = self.session.get(self._url(f"/library/sections/{library_key}/collections"), timeout=30)
        r.raise_for_status()
        if r.headers.get("Content-Type","").startswith("application/json"):
            return r.json()
        return []

    def add_collection_to_item(self, rating_key: str, collection: str):
        params = {"type": 1, "id": rating_key, "collection[0].tag.tag": collection}
        r = self.session.put(self._url("/library/sections/all"), params=params, timeout=30)
        r.raise_for_status()
        return True
