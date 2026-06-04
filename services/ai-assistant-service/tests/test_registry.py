"""Unit tests for provider registry and fallback logic."""
import pytest
import os
from unittest.mock import AsyncMock

from domain.ports import AIProviderPort
from providers.registry import ProviderRegistry


class MockProvider(AIProviderPort):
    def __init__(self, name: str, is_available: bool = True):
        self.name = name
        self._available = is_available
        
    async def is_available(self) -> bool:
        return self._available
        
    async def complete(self, *args, **kwargs):
        pass
        
    async def stream(self, *args, **kwargs):
        pass


@pytest.mark.asyncio
async def test_registry_returns_first_available():
    p1 = MockProvider("p1", is_available=False)
    p2 = MockProvider("p2", is_available=True)
    p3 = MockProvider("p3", is_available=True)
    
    registry = ProviderRegistry(chain=[p1, p2, p3])
    provider = await registry.get_provider()
    
    assert provider == p2
    assert provider.name == "p2"


@pytest.mark.asyncio
async def test_registry_falls_back_to_last_if_all_unavailable():
    p1 = MockProvider("p1", is_available=False)
    p2 = MockProvider("p2", is_available=False)
    
    registry = ProviderRegistry(chain=[p1, p2])
    provider = await registry.get_provider()
    
    # Should return the last one as a last resort
    assert provider == p2
    assert provider.name == "p2"
