"""
Provider registry — selects the active provider via AI_PROVIDER env var
and implements the cascading fallback chain.

Priority:
  configured provider → Ollama (always last resort)
"""
import os
import logging
from typing import List
from domain.models import AIProvider
from domain.ports import AIProviderPort

logger = logging.getLogger(__name__)

_AI_PROVIDER = os.getenv("AI_PROVIDER", "ollama").lower()


def _build_fallback_chain() -> List[AIProviderPort]:
    """Build the ordered provider chain based on configuration."""
    from providers.ollama_provider import OllamaProvider
    from providers.grok_provider import GrokProvider
    from providers.gemini_provider import GeminiProvider

    ollama = OllamaProvider()

    if _AI_PROVIDER == AIProvider.GROK:
        return [GrokProvider(), ollama]
    elif _AI_PROVIDER == AIProvider.GEMINI:
        return [GeminiProvider(), ollama]
    else:
        return [ollama]


class ProviderRegistry:
    """
    Selects the first available provider from the fallback chain.
    Thread-safe singleton via module-level instance.
    """

    def __init__(self, chain: List[AIProviderPort] = None):
        self._chain = chain or _build_fallback_chain()

    async def get_provider(self) -> AIProviderPort:
        """Return the first available provider, always falling back to Ollama."""
        for provider in self._chain:
            if await provider.is_available():
                return provider
        # Last resort: return the last in chain (always Ollama) even if it reports unavailable
        logger.warning("No provider reported available — returning last in chain")
        return self._chain[-1]
