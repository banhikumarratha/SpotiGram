"""
YouTube Data API v3 client.
All searches are locked to music content only:
  - videoCategoryId=10  → Music category
  - topicId=/m/04rlf   → Music topic
  - type=video          → Videos only (no playlists/channels)
"""
import httpx
import os
import logging
import re

logger = logging.getLogger(__name__)

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
MUSIC_CATEGORY_ID = "10"        # YouTube Music category
MUSIC_TOPIC_ID = "/m/04rlf"    # YouTube Music topic freebase ID


def _parse_duration(iso_duration: str) -> str:
    """Convert ISO 8601 duration (PT4M33S) to mm:ss string."""
    if not iso_duration:
        return ""
    match = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", iso_duration)
    if not match:
        return ""
    hours = int(match.group(1) or 0)
    minutes = int(match.group(2) or 0)
    seconds = int(match.group(3) or 0)
    if hours:
        return f"{hours}:{minutes:02d}:{seconds:02d}"
    return f"{minutes}:{seconds:02d}"


class YouTubeClient:
    def __init__(self):
        self.base_url = "https://www.googleapis.com/youtube/v3"

    async def search(self, query: str, limit: int = 20) -> dict:
        if not YOUTUBE_API_KEY:
            logger.error("YOUTUBE_API_KEY is not configured!")
            return {"tracks": {"items": []}}

        # Always append "music" or "official audio" if query doesn't imply it
        search_query = query if any(w in query.lower() for w in ["music", "song", "audio", "lyrics", "official"]) else f"{query} official music"

        params = {
            "part": "snippet",
            "q": search_query,
            "key": YOUTUBE_API_KEY,
            "type": "video",
            "videoCategoryId": MUSIC_CATEGORY_ID,  # Music videos only
            "topicId": MUSIC_TOPIC_ID,              # Must be music topic
            "maxResults": limit,
            "safeSearch": "none",
            "order": "relevance",
        }

        try:
            async with httpx.AsyncClient() as client:
                res = await client.get(
                    f"{self.base_url}/search", params=params, timeout=10.0
                )
                res.raise_for_status()
                data = res.json()

                video_ids = [
                    item["id"]["videoId"]
                    for item in data.get("items", [])
                    if item.get("id", {}).get("videoId")
                ]

                if not video_ids:
                    return {"tracks": {"items": []}}

                # Fetch full video details (duration, statistics, etc.)
                details = await self._get_video_details(client, video_ids)
                return {"tracks": {"items": details}}

        except Exception as e:
            logger.error(f"YouTube search request failed: {e}")
            return {"tracks": {"items": []}}

    async def _get_video_details(self, client: httpx.AsyncClient, video_ids: list) -> list:
        """Fetch snippet + contentDetails for a list of video IDs."""
        params = {
            "part": "snippet,contentDetails",
            "id": ",".join(video_ids),
            "key": YOUTUBE_API_KEY,
        }
        try:
            res = await client.get(
                f"{self.base_url}/videos", params=params, timeout=10.0
            )
            res.raise_for_status()
            data = res.json()
            items = []
            for item in data.get("items", []):
                video_id = item["id"]
                snippet = item.get("snippet", {})
                duration_raw = item.get("contentDetails", {}).get("duration", "")
                duration = _parse_duration(duration_raw)
                thumbnail = (
                    snippet.get("thumbnails", {})
                    .get("high", snippet.get("thumbnails", {}).get("default", {}))
                    .get("url", "")
                )
                items.append({
                    "id": video_id,
                    "name": snippet.get("title", "Unknown"),
                    "artists": [{"name": snippet.get("channelTitle", "Unknown Channel")}],
                    "duration": duration,
                    "album": {"images": [{"url": thumbnail}]},
                    "preview_url": f"https://www.youtube.com/watch?v={video_id}",
                })
            return items
        except Exception as e:
            logger.error(f"YouTube video details fetch failed: {e}")
            return []

    async def get_track(self, video_id: str) -> dict:
        if not YOUTUBE_API_KEY:
            logger.error("YOUTUBE_API_KEY is not configured!")
            return {}
        try:
            async with httpx.AsyncClient() as client:
                details = await self._get_video_details(client, [video_id])
                return details[0] if details else {}
        except Exception as e:
            logger.error(f"YouTube video lookup failed: {e}")
            return {}
