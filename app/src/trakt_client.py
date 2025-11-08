import os, requests
from typing import Iterable

TRAKT_API = "https://api.trakt.tv"

class TraktClient:
    def __init__(self):
        self.client_id = os.getenv("TRAKT_CLIENT_ID")
        self.client_secret = os.getenv("TRAKT_CLIENT_SECRET")
        self.access_token = os.getenv("TRAKT_ACCESS_TOKEN")
        if not self.client_id:
            raise ValueError("TRAKT_CLIENT_ID missing")
        if not self.access_token:
            raise ValueError("TRAKT_ACCESS_TOKEN missing")

    def _headers(self):
        return {
            "Content-Type": "application/json",
            "trakt-api-version": "2",
            "trakt-api-key": self.client_id,
            "Authorization": f"Bearer {self.access_token}",
        }

    def add_to_watchlist(self, imdb_ids: Iterable[str] = (), tmdb_ids: Iterable[int] = ()):
        payload = {"movies": []}
        for iid in imdb_ids:
            payload["movies"].append({"ids": {"imdb": iid}})
        for tid in tmdb_ids:
            payload["movies"].append({"ids": {"tmdb": int(tid)}})
        r = requests.post(f"{TRAKT_API}/sync/watchlist", headers=self._headers(), json=payload, timeout=30)
        r.raise_for_status()
        return r.json()

    def remove_from_watchlist(self, imdb_ids: Iterable[str] = (), tmdb_ids: Iterable[int] = ()):
        payload = {"movies": []}
        for iid in imdb_ids:
            payload["movies"].append({"ids": {"imdb": iid}})
        for tid in tmdb_ids:
            payload["movies"].append({"ids": {"tmdb": int(tid)}})
        r = requests.post(f"{TRAKT_API}/sync/watchlist/remove", headers=self._headers(), json=payload, timeout=30)
        r.raise_for_status()
        return r.json()

    def create_or_update_list(self, slug: str, name: str, description: str = "", privacy: str = "private"):
        r = requests.post(f"{TRAKT_API}/users/me/lists", headers=self._headers(),
                          json={"name": name, "description": description, "privacy": privacy, "display_numbers": False, "allow_comments": True}, timeout=30)
        if r.status_code not in (201, 409):
            r.raise_for_status()
        return True

    def add_movies_to_list(self, slug: str, imdb_ids: Iterable[str] = (), tmdb_ids: Iterable[int] = ()):
        payload = {"movies": []}
        for iid in imdb_ids:
            payload["movies"].append({"ids": {"imdb": iid}})
        for tid in tmdb_ids:
            payload["movies"].append({"ids": {"tmdb": int(tid)}})
        r = requests.post(f"{TRAKT_API}/users/me/lists/{slug}/items", headers=self._headers(), json=payload, timeout=30)
        r.raise_for_status()
        return r.json()
