from sqlalchemy.orm import Session
from sqlalchemy import text
import json
import logging
import time
import threading

logger = logging.getLogger("outbox")

class OutboxPublisher:
    def __init__(self, db_session_maker, kafka_producer):
        self.db_session_maker = db_session_maker
        self.kafka_producer = kafka_producer
        self._stop_event = threading.Event()

    def start_polling(self):
        def _poll():
            while not self._stop_event.is_set():
                try:
                    self._process_outbox()
                except Exception as e:
                    logger.error(f"Error processing outbox: {e}")
                time.sleep(2)
                
        thread = threading.Thread(target=_poll, daemon=True)
        thread.start()

    def stop_polling(self):
        self._stop_event.set()

    def _process_outbox(self):
        with self.db_session_maker() as session:
            # Postgres specific: SKIP LOCKED for concurrent workers
            result = session.execute(text(
                "SELECT id, aggregate_type, aggregate_id, type, payload FROM outbox_events WHERE processed = FALSE FOR UPDATE SKIP LOCKED LIMIT 50"
            ))
            events = result.fetchall()
            
            for event in events:
                topic = f"{event.aggregate_type}_events"
                # If publishing fails, we don't mark as processed
                self.kafka_producer.send(topic, key=str(event.aggregate_id).encode(), value=event.payload)
                
                # Mark processed
                session.execute(text("UPDATE outbox_events SET processed = TRUE WHERE id = :id"), {"id": event.id})
                
            session.commit()

# DLQ Handling Note:
# In Kafka consumers, wrap the message handler in a try/except block.
# If an unrecoverable error occurs (e.g., malformed payload), publish the raw message to `<topic>_dlq` and commit the offset.
