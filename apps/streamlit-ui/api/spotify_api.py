from api.client import APIClient
from utils.config import settings

class SpotifyAPI(APIClient):
    def __init__(self):
        super().__init__(settings.SPOTIFY_SERVICE_URL)

    def get_auth_url(self):
        return self.get("/api/v1/spotify/auth/url")

    def search(self, query: str):
        return self.get("/api/v1/spotify/search", params={"q": query})

    def get_devices(self):
        return self.get("/api/v1/spotify/player/devices")

    def play(self, context_uri: str = None, uris: list = None, device_id: str = None):
        payload = {}
        if context_uri:
            payload["context_uri"] = context_uri
        if uris:
            payload["uris"] = uris
            
        params = {}
        if device_id:
            params["device_id"] = device_id
            
        return self.put("/api/v1/spotify/player/play", json=payload if payload else None)

    def pause(self, device_id: str = None):
        return self.put("/api/v1/spotify/player/pause")
        
    def next_track(self, device_id: str = None):
        return self.post("/api/v1/spotify/player/next")
