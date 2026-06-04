"""
Ollama provider — local inference via REST API.
Default model: llama3.2 (fast, 3B). Fallback: mistral.
No API key required. Runs on localhost:11434.
"""
import os
import time
import json
import logging
from typing import Optional, AsyncIterator

import httpx

from domain.models import AIResponse, AIProvider
from providers.base import BaseProvider

logger = logging.getLogger(__name__)

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_DEFAULT_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")


class OllamaProvider(BaseProvider):
    """Connects to a locally running Ollama server."""

    def __init__(self, base_url: str = OLLAMA_BASE_URL, model: str = OLLAMA_DEFAULT_MODEL):
        self.base_url = base_url
        self.default_model = model

    async def is_available(self) -> bool:
        try:
            async with httpx.AsyncClient(timeout=3.0) as client:
                res = await client.get(f"{self.base_url}/api/tags")
                return res.status_code == 200
        except Exception:
            return False

    async def complete(
        self,
        prompt: str,
        system: str = "",
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1024,
    ) -> AIResponse:
        model = model or self.default_model
        start = time.monotonic()

        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": model,
            "messages": messages,
            "stream": False,
            "options": {"temperature": temperature, "num_predict": max_tokens},
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            res = await client.post(f"{self.base_url}/api/chat", json=payload)
            res.raise_for_status()
            data = res.json()

        content = data.get("message", {}).get("content", "")
        return self._timed_response(content, AIProvider.OLLAMA, model, start)

    async def stream(
        self,
        prompt: str,
        system: str = "",
        model: Optional[str] = None,
        temperature: float = 0.7,
    ) -> AsyncIterator[str]:
        model = model or self.default_model

        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": model,
            "messages": messages,
            "stream": True,
            "options": {"temperature": temperature},
        }

        async with httpx.AsyncClient(timeout=120.0) as client:
            async with client.stream("POST", f"{self.base_url}/api/chat", json=payload) as res:
                res.raise_for_status()
                async for line in res.aiter_lines():
                    if line:
                        try:
                            chunk = json.loads(line)
                            token = chunk.get("message", {}).get("content", "")
                            if token:
                                yield token
                        except json.JSONDecodeError:
                            continue
