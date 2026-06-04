"""Unit tests for the AssistantService."""
import pytest
from domain.models import UserContext, Role
from application.assistant_service import AssistantService


@pytest.mark.asyncio
async def test_assistant_chat_creates_new_conversation(fake_provider, memory_store):
    svc = AssistantService(fake_provider, memory_store)
    ctx = UserContext(user_id="u1", top_genres=["pop"])
    
    response = await svc.chat(user_id="u1", message="Hi", context=ctx)
    
    assert response.content == "Fake LLM response"
    assert response.provider.value == "ollama"
    assert memory_store.count() == 1
    
    # Check that it generated a uuid conversation_id since we didn't provide one
    convs = list(memory_store._store.values())
    conv = convs[0]
    assert conv.user_id == "u1"
    assert len(conv.messages) == 2
    assert conv.messages[0].role == Role.USER
    assert conv.messages[1].role == Role.ASSISTANT
    assert conv.messages[1].content == "Fake LLM response"


@pytest.mark.asyncio
async def test_assistant_chat_reuses_conversation(fake_provider, memory_store):
    svc = AssistantService(fake_provider, memory_store)
    
    # First turn
    res1 = await svc.chat(user_id="u1", message="Turn 1", conversation_id="conv_123")
    
    # Second turn
    res2 = await svc.chat(user_id="u1", message="Turn 2", conversation_id="conv_123")
    
    assert memory_store.count() == 1
    conv = await memory_store.get("conv_123")
    assert len(conv.messages) == 4


@pytest.mark.asyncio
async def test_assistant_stream(fake_provider, memory_store):
    svc = AssistantService(fake_provider, memory_store)
    
    tokens = []
    async for token in svc.stream(user_id="u1", message="Tell me a joke", conversation_id="conv_stream"):
        tokens.append(token)
        
    assert "".join(tokens) == "Fake LLM response "
    
    # Stream should also save to memory
    conv = await memory_store.get("conv_stream")
    assert conv is not None
    assert len(conv.messages) == 2
    assert conv.messages[1].role == Role.ASSISTANT
    assert conv.messages[1].content == "Fake LLM response "
