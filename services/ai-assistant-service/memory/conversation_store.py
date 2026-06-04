"""
In-memory conversation store — implements MemoryStorePort.
Swap-able for a Redis backend without changing application code.
"""
from typing import Dict, Optional
from domain.models import Conversation
from domain.ports import MemoryStorePort


class InMemoryConversationStore(MemoryStorePort):
    def __init__(self):
        self._store: Dict[str, Conversation] = {}

    async def get(self, conversation_id: str) -> Optional[Conversation]:
        return self._store.get(conversation_id)

    async def save(self, conversation: Conversation) -> None:
        self._store[conversation.conversation_id] = conversation

    async def delete(self, conversation_id: str) -> None:
        self._store.pop(conversation_id, None)

    def count(self) -> int:
        return len(self._store)
