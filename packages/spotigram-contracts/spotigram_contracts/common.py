from typing import Generic, TypeVar, Optional, List, Any
from pydantic import BaseModel, Field
from datetime import datetime

T = TypeVar('T')

class PaginationParams(BaseModel):
    limit: int = Field(20, ge=1, le=100)
    offset: int = Field(0, ge=0)
    cursor: Optional[str] = None

class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    next_cursor: Optional[str] = None

class StandardError(BaseModel):
    code: str
    message: str
    details: Optional[Any] = None

class StandardErrorEnvelope(BaseModel):
    error: StandardError
    correlation_id: str

class JwtClaimsSchema(BaseModel):
    sub: str
    roles: List[str] = Field(default_factory=list)
    exp: int

class EventHeaders(BaseModel):
    event_id: str
    correlation_id: str
    idempotency_key: str
    timestamp: datetime
    version: str = "v1"
