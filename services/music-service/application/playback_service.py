from infrastructure.kafka_publisher import KafkaPublisher
import uuid
from datetime import datetime

class PlaybackService:
    def __init__(self, publisher: KafkaPublisher = None):
        self.publisher = publisher

    async def emit_playback_event(self, user_id: str, track_id: str, action: str):
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
                    "action": action
                }
            }
            await self.publisher.publish(event)
        return {"status": "event_emitted", "action": action}
