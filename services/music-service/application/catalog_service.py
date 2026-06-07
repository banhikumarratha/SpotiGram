from infrastructure.youtube_client import YouTubeClient
from infrastructure.cache import get_from_cache, set_cache
import hashlib

class CatalogService:
    def __init__(self):
        self.youtube = YouTubeClient()

    async def search(self, query: str, search_type: str = "track") -> dict:
        cache_key = f"search:{search_type}:{hashlib.md5(query.encode()).hexdigest()}"
        cached = await get_from_cache(cache_key)
        if cached:
            return cached
            
        result = await self.youtube.search(query)
        await set_cache(cache_key, result, 3600)
        return result

    async def get_track(self, track_id: str) -> dict:
        cache_key = f"track:{track_id}"
        cached = await get_from_cache(cache_key)
        if cached:
            return cached
            
        result = await self.youtube.get_track(track_id)
        await set_cache(cache_key, result, 3600 * 24)
        return result

