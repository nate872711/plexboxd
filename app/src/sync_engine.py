import asyncio
import logging
from typing import Dict, Any, List

log = logging.getLogger("sync")

class SyncEngine:
    """
    Central place to orchestrate sync flows between Plex and other services.
    This is intentionally conservative/minimal: it logs what it would do
    and provides clear TODOs for enrichment/matching.
    """

    def __init__(self, services: Dict[str, Any], config: Dict[str, Any]):
        self.svcs = services
        self.cfg = config
        self.direction_spec = (self.cfg.get("general", {})
                                    .get("sync_direction", "plex->trakt,letterboxd,imdb"))

        # Parse direction like "plex->trakt,letterboxd,imdb"
        parts = self.direction_spec.split("->")
        self.source = parts[0].strip().lower() if len(parts) > 0 else "plex"
        self.destinations = []
        if len(parts) > 1:
            self.destinations = [d.strip().lower() for d in parts[1].split(",") if d.strip()]

        log.info(f"🔁 Sync direction: {self.source} -> {', '.join(self.destinations)}")

    async def sync_all(self):
        """
        Dispatch sync according to config.general.sync_direction.
        Currently supports source=plex. Extend as needed.
        """
        if self.source == "plex":
            await self._sync_from_plex()
        else:
            log.warning(f"Unsupported sync source: {self.source} (TODO)")

    async def _sync_from_plex(self):
        if "plex" not in self.svcs:
            log.warning("Plex is not initialized; skipping.")
            return

        log.info("📥 Fetching watched history from Plex…")
        plex_items = await self._get_plex_watched()
        log.info(f"✔ Plex items fetched: {len(plex_items)}")

        # Optional future: enrich with TMDb/TVDB metadata
        # plex_items = await self._enrich_items(plex_items)

        for dest in self.destinations:
            if dest == "trakt" and "trakt" in self.svcs:
                await self._push_to_trakt(plex_items)
            elif dest == "letterboxd" and "letterboxd" in self.svcs:
                await self._push_to_letterboxd(plex_items)
            elif dest == "imdb" and "imdb" in self.svcs:
                await self._push_to_imdb(plex_items)
            else:
                log.info(f"Skipping destination '{dest}' (not enabled or unsupported yet).")

    async def _get_plex_watched(self) -> List[dict]:
        """
        Convert Plex history objects into a normalized list of dicts:
        {title, year, type, watched_at, guid}
        """
        items = []
        try:
            # Plex API is sync; run in thread
            history = await asyncio.to_thread(self.svcs["plex"].get_watched)

            for entry in history:
                media = entry.ratingKey if hasattr(entry, "ratingKey") else None
                title = getattr(entry, "title", None) or getattr(entry, "grandparentTitle", None)
                year = getattr(entry, "year", None)
                watched_at = getattr(entry, "viewedAt", None)
                media_type = getattr(entry, "type", None)

                items.append({
                    "title": title,
                    "year": year,
                    "type": media_type,
                    "watched_at": watched_at,
                    "guid": media
                })
        except Exception as e:
            log.exception(f"Plex history fetch failed: {e}")

        return items

    async def _push_to_trakt(self, items: List[dict]):
        log.info("📤 Sync → Trakt (watched history)")
        try:
            # TODO: dedup, transform to Trakt's expected payload, call endpoints.
            # Placeholder: ensure token is valid and log what would be sent.
            watched = await self._sample(items, 5)
            log.info(f"Would push {len(items)} items to Trakt (showing first {len(watched)}): {watched}")
        except Exception as e:
            log.exception(f"Trakt push failed: {e}")

    async def _push_to_letterboxd(self, items: List[dict]):
        log.info("📤 Sync → Letterboxd (diary/logs)")
        try:
            films = [i for i in items if (i.get("type") == "movie" and i.get("title"))]
            sample = await self._sample(films, 5)
            log.info(f"Would push {len(films)} films to Letterboxd (first {len(sample)}): {sample}")
        except Exception as e:
            log.exception(f"Letterboxd push failed: {e}")

    async def _push_to_imdb(self, items: List[dict]):
        log.info("📤 Sync → IMDb (CSV-based import is read-only; push TBD)")
        try:
            # IMDb official export is CSV → read-only source typically.
            # Implement reverse (push) via 3rd-party if desired. Placeholder:
            log.info("IMDb push is not implemented; treat IMDb as a read-only source for now.")
        except Exception as e:
            log.exception(f"IMDb push failed: {e}")

    async def _enrich_items(self, items: List[dict]) -> List[dict]:
        """
        (Optional) Enrich with TMDb/TVDB lookups if enabled.
        """
        # Example idea:
        # if "tmdb" in self.svcs:
        #     for item in items:
        #         # call TMDb to attach ids/posters
        #         pass
        return items

    @staticmethod
    async def _sample(items: List[dict], n: int) -> List[dict]:
        return items[:n] if len(items) > n else items
