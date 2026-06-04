import os
import json
from typing import Dict, Any

KAFKA_URL = os.getenv("KAFKA_URL", "kafka:9092")
producer = None

async def get_kafka_producer():
    global producer
    if producer is None:
        from aiokafka import AIOKafkaProducer
        producer = AIOKafkaProducer(
            bootstrap_servers=KAFKA_URL,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        await producer.start()
    return producer

async def close_kafka_producer():
    global producer
    if producer is not None:
        await producer.stop()
        producer = None

class KafkaPublisher:
    def __init__(self, topic: str):
        self.topic = topic

    async def publish(self, event: Dict[str, Any]):
        prod = await get_kafka_producer()
        await prod.send_and_wait(self.topic, event)
