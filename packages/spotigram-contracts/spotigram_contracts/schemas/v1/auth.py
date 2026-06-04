from pydantic import BaseModel
from typing import Optional

class SpotifyTokenData(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    expires_in: int
    token_type: str = "Bearer"
