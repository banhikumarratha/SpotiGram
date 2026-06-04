"""
Base AI provider class with shared fallback + retry logic.
All concrete providers inherit from this.
"""
import time
import logging
from abc import ABC
from typing import Optional
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import httpx

from domain.models import AIResponse, AIProvider
from domain.ports import AIProviderPort

logger = logging.getLogger(__name__)

PROMPT_VERSION = "v1"


class BaseProvider(AIProviderPort, ABC):
    """Shared retry decorator and timing helpers for all providers."""

    def _timed_response(
        self,
        content: str,
        provider: AIProvider,
        model: str,
        start_time: float,
        prompt_version: str = PROMPT_VERSION,
        usage: dict = None,
    ) -> AIResponse:
        return AIResponse(
            content=content,
            provider=provider,
            model=model,
            prompt_version=prompt_version,
            usage=usage or {},
            latency_ms=round((time.monotonic() - start_time) * 1000, 2),
        )
