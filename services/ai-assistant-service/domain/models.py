"""
Domain models for the ai-assistant-service.
Pure dataclasses — no LangChain or framework imports.
"""
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from enum import Enum
from datetime import datetime


class Role(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class AIProvider(str, Enum):
    OLLAMA = "ollama"
    GROK = "grok"
    GEMINI = "gemini"


@dataclass
class Message:
    role: Role
    content: str
    timestamp: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Conversation:
    conversation_id: str
    user_id: str
    messages: List[Message] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    provider: AIProvider = AIProvider.OLLAMA

    def add_message(self, role: Role, content: str) -> None:
        self.messages.append(Message(role=role, content=content))

    def history_text(self) -> str:
        return "\n".join(f"{m.role.value}: {m.content}" for m in self.messages[-20:])


@dataclass
class UserContext:
    """
    Caller-provided context passed in each request.
    Loaded from the recommendation-service output — no cross-DB calls needed.
    """
    user_id: str
    top_genres: List[str] = field(default_factory=list)
    top_artists: List[str] = field(default_factory=list)
    current_mood: Optional[str] = None
    recent_tracks: List[str] = field(default_factory=list)
    preferences: Dict[str, Any] = field(default_factory=dict)

    def as_context_string(self) -> str:
        parts = [f"User: {self.user_id}"]
        if self.top_genres:
            parts.append(f"Favorite genres: {', '.join(self.top_genres[:5])}")
        if self.top_artists:
            parts.append(f"Favorite artists: {', '.join(self.top_artists[:5])}")
        if self.current_mood:
            parts.append(f"Current mood: {self.current_mood}")
        if self.recent_tracks:
            parts.append(f"Recently played: {', '.join(self.recent_tracks[:5])}")
        return "\n".join(parts)


@dataclass
class AIResponse:
    content: str
    provider: AIProvider
    model: str
    prompt_version: str
    usage: Dict[str, int] = field(default_factory=dict)
    structured: Optional[Dict[str, Any]] = None
    latency_ms: float = 0.0


@dataclass
class GeneratedPlaylist:
    name: str
    description: str
    track_queries: List[str]  # Natural-language track search queries
    reasoning: str
    mood: Optional[str] = None


@dataclass
class DJSession:
    session_id: str
    user_id: str
    current_track: Optional[str] = None
    mood: Optional[str] = None
    messages: List[Message] = field(default_factory=list)
    state: str = "idle"  # idle | playing | transitioning | paused
    created_at: datetime = field(default_factory=datetime.utcnow)
