from pydantic import BaseModel
from typing import List, Dict

class TasteVector(BaseModel):
    acousticness: float
    danceability: float
    energy: float
    valence: float
    tempo: float

class MusicDNA(BaseModel):
    user_id: str
    top_genres: List[str]
    taste_vector: TasteVector
    calculated_at: str
