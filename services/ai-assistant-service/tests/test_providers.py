"""Unit tests for concrete providers using mocks."""
import pytest
from unittest.mock import AsyncMock, patch, MagicMock

from providers.ollama_provider import OllamaProvider
from providers.grok_provider import GrokProvider
from providers.gemini_provider import GeminiProvider


@pytest.mark.asyncio
async def test_ollama_provider_complete():
    provider = OllamaProvider()
    with patch("httpx.AsyncClient") as mock_client_cls:
        mock_client = AsyncMock()
        mock_client_cls.return_value.__aenter__.return_value = mock_client
        mock_response = MagicMock()
        mock_response.json.return_value = {"message": {"content": "Ollama response"}}
        mock_client.post.return_value = mock_response
        
        res = await provider.complete("Hello")
        assert res.content == "Ollama response"
        assert res.provider.value == "ollama"


@pytest.mark.asyncio
async def test_grok_provider_is_available():
    provider = GrokProvider(api_key="test_key")
    assert await provider.is_available() is True
    
    provider_no_key = GrokProvider(api_key="")
    assert await provider_no_key.is_available() is False


@pytest.mark.asyncio
async def test_gemini_provider_is_available():
    provider = GeminiProvider(api_key="test_key")
    assert await provider.is_available() is True
    
    provider_no_key = GeminiProvider(api_key="")
    assert await provider_no_key.is_available() is False
