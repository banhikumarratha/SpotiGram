import json
import logging
from abc import ABC, abstractmethod
from typing import List, Callable, Awaitable
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer

logger = logging.getLogger(__name__)

class DLQKafkaConsumer(ABC):
    """
    Abstract Kafka Consumer that handles Dead Letter Queues (DLQ).
    """
    def __init__(self, bootstrap_servers: str, group_id: str, topics: List[str], dlq_topic: str = "spotigram.dlq"):
        self.bootstrap_servers = bootstrap_servers
        self.group_id = group_id
        self.topics = topics
        self.dlq_topic = dlq_topic
        self.consumer = None
        self.producer = None
        
    async def start(self):
        self.consumer = AIOKafkaConsumer(
            *self.topics,
            bootstrap_servers=self.bootstrap_servers,
            group_id=self.group_id,
            value_deserializer=lambda m: json.loads(m.decode('utf-8'))
        )
        self.producer = AIOKafkaProducer(
            bootstrap_servers=self.bootstrap_servers,
            value_serializer=lambda m: json.dumps(m).encode('utf-8')
        )
        await self.consumer.start()
        await self.producer.start()
        logger.info(f"Consumer started for topics: {self.topics}. DLQ routing enabled.")

    async def stop(self):
        if self.consumer:
            await self.consumer.stop()
        if self.producer:
            await self.producer.stop()

    @abstractmethod
    async def process_message(self, topic: str, message_value: dict):
        pass

    async def consume(self):
        try:
            async for msg in self.consumer:
                try:
                    await self.process_message(msg.topic, msg.value)
                except Exception as e:
                    logger.error(f"Failed to process message from {msg.topic}: {e}. Sending to DLQ.")
                    # Attach error context to the message before sending to DLQ
                    dlq_message = {
                        "original_topic": msg.topic,
                        "error": str(e),
                        "payload": msg.value
                    }
                    await self.producer.send_and_wait(self.dlq_topic, dlq_message)
        except Exception as e:
            logger.error(f"Consumer loop failed: {e}")
