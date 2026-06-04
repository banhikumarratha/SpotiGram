"""
Kafka consumer for user.events.v1 and music.events.v1.
Runs as a background asyncio task, updating Music DNA on every interaction.
"""
import asyncio
import json
import logging
import os
from datetime import datetime

from domain.models import InteractionType, MusicInteractionEvent

logger = logging.getLogger(__name__)

KAFKA_URL = os.getenv("KAFKA_URL", "kafka:9092")
TOPICS = ["user.events.v1", "music.events.v1"]


async def start_consumer(dna_service):
    """
    Starts an AIOKafka consumer in the background.
    dna_service is injected to avoid circular imports.
    """
    try:
        from aiokafka import AIOKafkaConsumer
        consumer = AIOKafkaConsumer(
            *TOPICS,
            bootstrap_servers=KAFKA_URL,
            group_id="recommendation-service",
            value_deserializer=lambda m: json.loads(m.decode("utf-8")),
            auto_offset_reset="earliest",
        )
        await consumer.start()
        logger.info("Kafka consumer started, listening on: %s", TOPICS)
        try:
            async for msg in consumer:
                await _handle(msg.value, dna_service)
        finally:
            await consumer.stop()
    except Exception as e:
        logger.warning("Kafka consumer unavailable (running without Kafka): %s", e)


async def _handle(event: dict, dna_service) -> None:
    """Route inbound events to the appropriate DNA update."""
    try:
        payload = event.get("payload", {})
        action = payload.get("action")

        # music.events.v1 — playback interaction
        if action in ("play", "like", "save", "skip", "share"):
            interaction = MusicInteractionEvent(
                user_id=payload.get("user_id", ""),
                track_id=payload.get("track_id", ""),
                action=InteractionType(action),
                timestamp=datetime.utcnow(),
                track_title=payload.get("track_title", ""),
                track_artist=payload.get("track_artist", ""),
                track_genres=payload.get("track_genres", []),
            )
            await dna_service.process_interaction(interaction)
    except Exception as e:
        logger.error("Error handling Kafka event: %s", e)
