from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class ErrorDetail(BaseModel):
    code: str
    message: str
    details: Optional[Dict[str, Any]] = None

class ErrorResponse(BaseModel):
    success: bool = False
    error: ErrorDetail

class PaginationMetadata(BaseModel):
    total: int
    limit: int
    offset: int
    next_cursor: Optional[str] = None

class TokenClaims(BaseModel):
    sub: str  # User ID
    exp: int
    iat: int
    roles: list[str] = Field(default_factory=list)
