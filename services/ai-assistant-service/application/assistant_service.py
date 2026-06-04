"""
AssistantService — orchestrates chat, RAG, memory, and streaming.
"""
import uuid
from typing import Optional, AsyncIterator

from domain.models import Conversation, Role, UserContext, AIResponse
from domain.ports import AIProviderPort, MemoryStorePort
from chains.rag_chain import run_rag_chain
from infrastructure.prompt_loader import get_system_prompt


class AssistantService:
    def __init__(self, provider: AIProviderPort, memory: MemoryStorePort):
        self._provider = provider
        self._memory = memory

    async def _get_or_create_conversation(
        self, conversation_id: Optional[str], user_id: str
    ) -> Conversation:
        if conversation_id:
            conv = await self._memory.get(conversation_id)
            if conv:
                return conv
        new_conv = Conversation(
            conversation_id=conversation_id or str(uuid.uuid4()),
            user_id=user_id,
        )
        await self._memory.save(new_conv)
        return new_conv

    async def chat(
        self,
        user_id: str,
        message: str,
        context: Optional[UserContext] = None,
        conversation_id: Optional[str] = None,
        prompt_version: str = "v1",
    ) -> AIResponse:
        """Single-turn chat with memory."""
        conv = await self._get_or_create_conversation(conversation_id, user_id)
        conv.add_message(Role.USER, message)

        response = await run_rag_chain(
            question=message,
            provider=self._provider,
            context=context,
            history=conv.history_text(),
            prompt_version=prompt_version,
        )

        conv.add_message(Role.ASSISTANT, response.content)
        await self._memory.save(conv)
        return response

    async def stream(
        self,
        user_id: str,
        message: str,
        context: Optional[UserContext] = None,
        conversation_id: Optional[str] = None,
    ) -> AsyncIterator[str]:
        """Streaming token-by-token response."""
        conv = await self._get_or_create_conversation(conversation_id, user_id)
        conv.add_message(Role.USER, message)

        system = get_system_prompt("query")
        context_str = context.as_context_string() if context else "No context."
        full_prompt = f"Context:\n{context_str}\n\nHistory:\n{conv.history_text()}\n\nQuestion: {message}"

        collected = []
        async for token in self._provider.stream(prompt=full_prompt, system=system):
            collected.append(token)
            yield token

        # Save full response to memory after streaming completes
        conv.add_message(Role.ASSISTANT, "".join(collected))
        await self._memory.save(conv)
