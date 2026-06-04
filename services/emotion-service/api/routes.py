from fastapi import APIRouter
from pydantic import BaseModel
from libs.shared.enums import Mood
from application.emotion_logic import EmotionLogic

router = APIRouter(prefix="/api/v1/emotion", tags=["Emotion"])
logic = EmotionLogic()

class AnalyzeRequest(BaseModel):
    text: str

class AnalyzeResponse(BaseModel):
    mood: Mood

@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_emotion(req: AnalyzeRequest):
    mood = logic.analyze_text(req.text)
    return AnalyzeResponse(mood=mood)
