from sqlalchemy import Column, String, DateTime, JSON
from infrastructure.database.session import Base
import uuid
from datetime import datetime

class PostRecord(Base):
    __tablename__ = "posts"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, index=True, nullable=False)
    track = Column(JSON, nullable=False) # Store track info as JSON
    caption = Column(String, nullable=True)
    mood = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
