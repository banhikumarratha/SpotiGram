import httpx
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import os
import base64

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID", "mock_client_id")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET", "mock_client_secret")

class SpotifyClientError(Exception):
    pass

class SpotifyClient:
    def __init__(self):
        self.base_url = "https://api.spotify.com/v1"
        self.auth_url = "https://accounts.spotify.com/api/token"

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((httpx.RequestError, httpx.TimeoutException))
    )
    async def get_client_credentials_token(self) -> str:
        if SPOTIFY_CLIENT_ID == "mock_client_id":
            return "mock_token"
        
        auth_str = f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}"
        b64_auth_str = base64.b64encode(auth_str.encode()).decode()
        
        headers = {
            "Authorization": f"Basic {b64_auth_str}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {"grant_type": "client_credentials"}
        
        async with httpx.AsyncClient() as client:
            res = await client.post(self.auth_url, headers=headers, data=data, timeout=10.0)
            if res.status_code != 200:
                raise SpotifyClientError(f"Failed to get token: {res.text}")
            return res.json()["access_token"]

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((httpx.RequestError, httpx.TimeoutException))
    )
    async def search(self, token: str, query: str, type: str = "track", limit: int = 20) -> dict:
        if token == "mock_token":
            return {
                "tracks": {
                    "items": [
                        {"id": "mock_track_1", "name": f"Mock Track for {query}", "artists": [{"name": "Mock Artist"}]}
                    ]
                }
            }
        
        headers = {"Authorization": f"Bearer {token}"}
        params = {"q": query, "type": type, "limit": limit}
        
        async with httpx.AsyncClient() as client:
            res = await client.get(f"{self.base_url}/search", headers=headers, params=params, timeout=10.0)
            if res.status_code == 401:
                raise SpotifyClientError("Unauthorized: Token expired")
            res.raise_for_status()
            return res.json()

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((httpx.RequestError, httpx.TimeoutException))
    )
    async def get_track(self, token: str, track_id: str) -> dict:
        if token == "mock_token":
            return {"id": track_id, "name": "Mock Track", "artists": [{"name": "Mock Artist"}]}
            
        headers = {"Authorization": f"Bearer {token}"}
        
        async with httpx.AsyncClient() as client:
            res = await client.get(f"{self.base_url}/tracks/{track_id}", headers=headers, timeout=10.0)
            res.raise_for_status()
            return res.json()
