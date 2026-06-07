from infrastructure.kafka_publisher import KafkaPublisher
import uuid
from datetime import datetime

class PlaybackService:
    def __init__(self, publisher: KafkaPublisher = None):
        self.publisher = publisher

    async def emit_playback_event(self, user_id: str, track_id: str, action: str):
        track_title = ""
        track_artist = ""
        track_genres = []
        try:
            from application.catalog_service import CatalogService
            catalog = CatalogService()
            track = await catalog.get_track(track_id)
            if track:
                track_title = track.get("name", "")
                artists = track.get("artists", [])
                if artists:
                    track_artist = artists[0].get("name", "")
                
                # Inferred genres from track title
                title_lower = track_title.lower()
                for g in ["pop", "indie", "electronic", "hip-hop", "hiphop", "rock", "jazz", "classical", "lofi", "chill"]:
                    if g in title_lower:
                        genre_name = "hip-hop" if g in ("hip-hop", "hiphop") else g
                        track_genres.append(genre_name)
                if not track_genres:
                    track_genres = ["pop"]
        except Exception:
            pass

        if self.publisher:
            event = {
                "headers": {
                    "event_id": str(uuid.uuid4()),
                    "correlation_id": "none",
                    "idempotency_key": str(uuid.uuid4()),
                    "timestamp": datetime.utcnow().isoformat(),
                    "version": "v1"
                },
                "payload": {
                    "user_id": user_id,
                    "track_id": track_id,
                    "action": action,
                    "track_title": track_title,
                    "track_artist": track_artist,
                    "track_genres": track_genres,
                }
            }
            await self.publisher.publish(event)
        return {"status": "event_emitted", "action": action}
