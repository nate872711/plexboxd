import logging
import asyncio
from trakt import Trakt
import httpx

log = logging.getLogger("trakt")

class TraktClient:
    """
    Works with the modern trakt.py client.
    Authentication is done via provided access/refresh tokens.
    """

    def __init__(self, client_id, client_secret, access_token, refresh_token):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = access_token
        self.refresh_token = refresh_token

        # Set client defaults
        Trakt.configuration.defaults.client(
            id=self.client_id,
            secret=self.client_secret
        )

        # Set OAuth token & refresh method
        Trakt.configuration.defaults.oauth(
            token=self.access_token,
            refresh=self._refresh_token  # callback
        )

    async def authenticate(self):
        """
        Validates the token by making a benign API call.
        If it fails, we attempt token refresh.
        """
        log.info("🔐 Authenticating Trakt token…")

        try:
            user = await asyncio.to_thread(Trakt['users/settings'].get)
            if user:
                log.info(f"✔ Trakt authenticated as: {user['user']['username']}")
                return True

        except Exception as e:
            log.warning(f"⚠ Trakt token invalid or expired: {e}")

        # Try refresh if needed
        return await self._refresh_token()

    async def _refresh_token(self):
        """
        Refresh access token using refresh_token.
        """
        if not self.refresh_token:
            log.error("❌ No refresh token available—cannot refresh.")
            return False

        log.info("🔄 Refreshing Trakt OAuth token…")
        try:
            # Raw HTTP call required (Trakt API token endpoint)
            async with httpx.AsyncClient(timeout=10) as client:
                r = await client.post(
                    "https://api.trakt.tv/oauth/token",
                    json={
                        "refresh_token": self.refresh_token,
                        "client_id": self.client_id,
                        "client_secret": self.client_secret,
                        "redirect_uri": "urn:ietf:wg:oauth:2.0:oob",
                        "grant_type": "refresh_token"
                    }
                )

            if r.status_code != 200:
                log.error(f"❌ Trakt token refresh failed: {r.text}")
                return False

            data = r.json()
            self.access_token = data["access_token"]
            self.refresh_token = data["refresh_token"]

            # Apply new tokens to Trakt client
            Trakt.configuration.defaults.oauth(
                token=self.access_token,
                refresh=self._refresh_token
            )

            log.info("✔ Trakt token refreshed successfully.")
            return True

        except Exception as e:
            log.exception(f"❌ Exception refreshing Trakt token: {e}")
            return False

    #
    # You can expand these later
    #
    async def get_watched(self):
        """Example: pull watched from Trakt (currently unused)."""
        try:
            return await asyncio.to_thread(Trakt['sync/history'].get)
        except Exception as e:
            log.error(f"Trakt history fetch failed: {e}")
            return []
