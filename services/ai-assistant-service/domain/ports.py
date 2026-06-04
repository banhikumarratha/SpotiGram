"""
Domain ports (abstract interfaces) for the ai-assistant-service.
Application logic depends only on these — never on concrete providers.
"""
from abc import ABC, abstractmethod
from typing import List, Optional, AsyncIterator, Dict, Any
from domain.models import Conversation, AIResponse, UserContext, GeneratedPlaylist


class AIProviderPort(ABC):
    """Core LLM provider interface."""

    @abstractmethod
    async def complete(
        self,
        prompt: str,
        system: str = "",
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1024,
    ) -> AIResponse:
        """Single-turn completion."""
        ...

    @abstractmethod
    async def stream(
        self,
        prompt: str,
        system: str = "",
        model: Optional[str] = None,
        temperature: float = 0.7,
    ) -> AsyncIterator[str]:
        """Streaming token-by-token completion."""
        ...

    @abstractmethod
    async def is_available(self) -> bool:
        """Health check for the provider endpoint."""
        ...


class MemoryStorePort(ABC):
    """Port for conversation persistence."""

    @abstractmethod
    async def get(self, conversation_id: str) -> Optional[Conversation]:
        ...

    @abstractmethod
    async def save(self, conversation: Conversation) -> None:
        ...

    @abstractmethod
    async def delete(self, conversation_id: str) -> None:
        ...
