# ADR-005: Multi-Provider AI with Fallback

**Date**: 2025-03-15
**Status**: Accepted

## Context
Relying on a single LLM provider creates a single point of failure. Ollama may be slow, Grok or Gemini API keys may expire.

## Decision
The ai-assistant-service implements a `ProviderRegistry` that supports multiple AI providers (Ollama, Grok, Gemini) with automatic fallback. The default provider is Ollama (local, free), with cloud providers as fallbacks.

## Consequences
- The AI DJ continues working even if the primary provider is down
- Each provider implements the same `AIProviderPort` interface
- Provider selection can be configured per-request or globally via environment variables
