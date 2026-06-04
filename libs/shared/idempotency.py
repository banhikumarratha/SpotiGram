import redis

class IdempotencyGuard:
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client

    def is_processed(self, event_id: str) -> bool:
        """Check if an event ID has already been processed."""
        return self.redis.exists(f"processed_events:{event_id}") > 0

    def mark_processed(self, event_id: str, ttl_seconds: int = 86400 * 7):
        """Mark an event ID as processed with a TTL (e.g. 7 days)."""
        self.redis.setex(f"processed_events:{event_id}", ttl_seconds, "1")
