"""
Kafka publisher adapter — implements EventPublisherPort.
Publishes recommendation.events.v1 messages.
"""
import os
import json
from typing import Dict, Any
from domain.ports import EventPublisherPort

KAFKA_URL = os.getenv("KAFKA_URL", "kafka:9092")
RECOMMENDATIONS_TOPIC = "recommendation.events.v1"

_producer = None


async def _get_producer():
    global _producer
    if _producer is None:
        from aiokafka import AIOKafkaProducer
        _producer = AIOKafkaProducer(
            bootstrap_servers=KAFKA_URL,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        )
        await _producer.start()
    return _producer


async def close_kafka_producer():
    global _producer
    if _producer is not None:
        await _producer.stop()
        _producer = None


class KafkaRecommendationPublisher(EventPublisherPort):
    def __init__(self, topic: str = RECOMMENDATIONS_TOPIC):
        self.topic = topic

    async def publish(self, event: Dict[str, Any]) -> None:
        prod = await _get_producer()
        await prod.send_and_wait(self.topic, event)
