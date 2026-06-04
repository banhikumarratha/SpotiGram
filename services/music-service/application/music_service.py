from libs.shared.schemas.domain import TrackInfo
from typing import Optional

class MusicService:
    def get_track_info(self, track_id: str) -> Optional[TrackInfo]:
        # Mocking Spotify API call
        if track_id == "notfound":
            return None
        return TrackInfo(
            spotify_id=track_id,
            title=f"Mocked Title for {track_id}",
            artist="Mocked Artist",
            duration_ms=180000
        )
