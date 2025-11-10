import logging
import httpx

log = logging.getLogger("tvdb")

class TheTVDBClient:
    BASE = "https://api4.thetvdb.com/v4"

    def __init__(self, api_key: str, pin: str):
        self.api_key = api_key
        self.pin = pin
        self.token = None

    async def authenticate(self) -> bool:
        url = f"{self.BASE}/login"
        payload = {"apikey": self.api_key, "pin": self.pin}
        try:
            async with httpx.AsyncClient(timeout=15) as client:
                r = await client.post(url, json=payload)
                r.raise_for_status()
                data = r.json()
            self.token = data.get("data", {}).get("token")
            if not self.token:
                log.error(f"TheTVDB auth error: {data}")
                return False
            log.info("TheTVDB authenticated")
            return True
        except Exception as e:
            log.exception(f"TheTVDB auth exception: {e}")
            return False

    async def _get(self, endpoint: str):
        if not self.token:
            log.warning("TheTVDB not authenticated")
            return None
        headers = {"Authorization": f"Bearer {self.token}"}
        url = f"{self.BASE}{endpoint}"
        async with httpx.AsyncClient(timeout=20) as client:
            r = await client.get(url, headers=headers)
            r.raise_for_status()
            return r.json()

    async def search(self, query: str):
        try:
            return await self._get(f"/search?query={query}")
        except Exception as e:
            log.exception(f"TheTVDB search error: {e}")
            return {}

    async def get_series(self, tvdb_id: int):
        try:
            return await self._get(f"/series/{tvdb_id}")
        except Exception as e:
            log.exception(f"TheTVDB series error: {e}")
            return {}
