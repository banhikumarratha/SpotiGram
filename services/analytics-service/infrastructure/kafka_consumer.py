import os
import json
import asyncio
from aiokafka import AIOKafkaConsumer

from domain.ports import EventConsumerPort


class KafkaEventConsumer(EventConsumerPort):
    def __init__(self, handler, bootstrap_servers: str = None):
        self.handler = handler
        self.bootstrap_servers = bootstrap_servers or os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
        self.topics = ["music.events.v1", "music.interactions.v1", "moods.events.v1", "mood.detected.v1", "recommendation.events.v1"]
        self.consumer = None
        self.task = None

    async def start(self):
        self.consumer = AIOKafkaConsumer(
            *self.topics,
            bootstrap_servers=self.bootstrap_servers,
            group_id="analytics-service-group",
            value_deserializer=lambda m: json.loads(m.decode("utf-8")),
            auto_offset_reset="earliest",
        )
        await self.consumer.start()
        self.task = asyncio.create_task(self._consume_loop())

    async def stop(self):
        if self.task:
            self.task.cancel()
        if self.consumer:
            await self.consumer.stop()

    async def _consume_loop(self):
        try:
            async for msg in self.consumer:
                topic = msg.topic
                data = msg.value
                try:
                    await self.handler.handle_event(topic, data)
                except Exception as e:
                    print(f"Error handling event {topic}: {e}")
        except asyncio.CancelledError:
            pass
