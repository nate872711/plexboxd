import asyncio
from trakt import init, Trakt
from rich import print


class TraktClient:
    def __init__(self, client_id, client_secret, access_token, refresh_token):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = access_token
        self.refresh_token = refresh_token

        init(client_id=self.client_id, client_secret=self.client_secret)

    async def authenticate(self):
        """Ensures Trakt OAuth credentials are valid."""
        try:
            Trakt.configuration.defaults.app(
                id=self.client_id,
                secret=self.client_secret
            )

            Trakt.configuration.defaults.oauth(
                token=self.access_token,
                refresh=self.refresh_token
            )

            print("[green]Trakt authentication validated")
        except Exception as e:
            print(f"[red]Trakt auth failed: {e}")

    async def get_watched(self):
        try:
            return Trakt['sync/history'].get()
        except Exception as e:
            print(f"[red]Trakt get_watched error: {e}")
            return []
