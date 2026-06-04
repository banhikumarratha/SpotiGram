from pydantic import BaseModel
from typing import Optional

class DocumentMetadata(BaseModel):
    doc_id: str
    user_id: Optional[str] = None
    type: str # e.g. "post", "track_embedding"
    tags: list[str] = []
