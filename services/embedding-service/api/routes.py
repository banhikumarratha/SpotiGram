from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from application.embedding_logic import EmbeddingLogic

router = APIRouter(prefix="/api/v1/embedding", tags=["Embedding"])
logic = EmbeddingLogic()

class EmbedRequest(BaseModel):
    text: str

class EmbedResponse(BaseModel):
    vector: List[float]

@router.post("/generate", response_model=EmbedResponse)
async def generate_embedding(req: EmbedRequest):
    vector = logic.generate_embedding(req.text)
    return EmbedResponse(vector=vector)
