# ADR-002: AI Sandbox — LangChain Isolation

**Date**: 2025-02-01
**Status**: Accepted

## Context
LangChain and LangGraph are powerful but complex frameworks. Allowing them in every service would couple business logic to a rapidly-evolving framework and make testing difficult.

## Decision
LangChain and LangGraph are permitted **only** inside `services/ai-assistant-service`. All other services must interact with AI capabilities via the AI service's REST API. This boundary is enforced by automated architecture fitness tests (`tests/architecture/test_fitness.py`) that parse Python AST and fail CI if any `langchain` or `langgraph` import is found outside the sandbox.

## Consequences
- AI framework upgrades are isolated to a single service
- Other services remain framework-agnostic
- AI domain models are pure dataclasses (no LangChain types leak)
- Testing is simpler — mock the AI service API, not LangChain internals
