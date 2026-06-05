import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.orm import declarative_mixin

@declarative_mixin
class OutboxEventMixin:
    """
    SQLAlchemy Mixin for the Outbox Pattern.
    Services should inherit from this to create an 'outbox_events' table.
    """
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    topic = Column(String(255), nullable=False)
    payload = Column(Text, nullable=False) # JSON encoded payload
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    processed_at = Column(DateTime, nullable=True) # Null if not processed yet
