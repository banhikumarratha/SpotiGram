from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Enum as SQLEnum, Text, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from .database import Base
import uuid

class AccountStatus(str, enum.Enum):
    PENDING_VERIFICATION = "PENDING_VERIFICATION"
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    DELETED = "DELETED"

class ConnectionStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    BLOCKED = "BLOCKED"
    MUTED = "MUTED"

def generate_uuid():
    return str(uuid.uuid4())

class UserAccount(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=generate_uuid)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    status = Column(SQLEnum(AccountStatus), default=AccountStatus.ACTIVE, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class UserProfile(Base):
    __tablename__ = "profiles"
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    display_name = Column(String, nullable=False)
    bio = Column(Text, nullable=True)
    avatar_url = Column(String, nullable=True)
    privacy_status = Column(String, default="PUBLIC")
    
    user = relationship("UserAccount")

class Connection(Base):
    __tablename__ = "connections"
    id = Column(String, primary_key=True, default=generate_uuid)
    follower_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    followed_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    status = Column(SQLEnum(ConnectionStatus), default=ConnectionStatus.ACTIVE)
    timestamp = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("follower_id", "followed_id", name="uix_follower_followed"),
    )
