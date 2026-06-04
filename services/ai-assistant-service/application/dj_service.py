"""
DJService — manages AI DJ sessions using the LangGraph workflow.
"""
import uuid
from typing import Optional

from domain.models import DJSession, UserContext
from domain.ports import AIProviderPort
from workflows.dj_workflow import run_dj_workflow


_sessions: dict = {}  # In-process session store


class DJService:
    def __init__(self, provider: AIProviderPort):
        self._provider = provider

    async def start_session(self, user_id: str, mood: Optional[str] = None) -> DJSession:
        session = DJSession(
            session_id=str(uuid.uuid4()),
            user_id=user_id,
            mood=mood or "neutral",
        )
        _sessions[session.session_id] = session
        return session

    async def interact(
        self,
        session_id: str,
        user_message: str,
        context: Optional[UserContext] = None,
        current_track: Optional[str] = None,
    ) -> str:
        session = _sessions.get(session_id)
        if not session:
            # Auto-create session if not found
            session = DJSession(session_id=session_id, user_id="unknown")
            _sessions[session_id] = session

        if current_track:
            session.current_track = current_track

        context_str = context.as_context_string() if context else "No user context."
        response = await run_dj_workflow(
            user_message=user_message,
            context_str=context_str,
            current_track=session.current_track or "",
            mood=session.mood or "neutral",
            provider=self._provider,
        )

        session.state = "playing"
        _sessions[session_id] = session
        return response
