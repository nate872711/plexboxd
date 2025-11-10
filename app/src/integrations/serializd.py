import logging
import httpx

log = logging.getLogger("serializd")

class SerializdClient:
    BASE = "https://api.serializd.com"

    def __init__(self, api_key: str):
        self.api_key = api_key

    async def get_activity(self):
        url = f"{self.BASE}/v1/activity"
        try:
            async with httpx.AsyncClient(timeout=15) as client:
                r = await client.get(url, headers={"Authorization": f"Bearer {self.api_key}"})
                r.raise_for_status()
                return r.json()
        except Exception as e:
            log.exception(f"Serializd error: {e}")
            return {}
