from infrastructure.spotify_client import SpotifyClient, SpotifyClientError
from infrastructure.cache import get_from_cache, set_cache
import hashlib

class CatalogService:
    def __init__(self):
        self.spotify = SpotifyClient()

    async def _get_token(self) -> str:
        token = await get_from_cache("spotify_client_token")
        if not token:
            token = await self.spotify.get_client_credentials_token()
            await set_cache("spotify_client_token", token, 3500)
        return token

    async def search(self, query: str, search_type: str = "track") -> dict:
        cache_key = f"search:{search_type}:{hashlib.md5(query.encode()).hexdigest()}"
        cached = await get_from_cache(cache_key)
        if cached:
            return cached
            
        token = await self._get_token()
        result = await self.spotify.search(token, query, search_type)
        
        await set_cache(cache_key, result, 3600)
        return result

    async def get_track(self, track_id: str) -> dict:
        cache_key = f"track:{track_id}"
        cached = await get_from_cache(cache_key)
        if cached:
            return cached
            
        token = await self._get_token()
        result = await self.spotify.get_track(token, track_id)
            
        await set_cache(cache_key, result, 3600 * 24)
        return result
