# ADR 002: LangChain and LangGraph Constraints

**Status:** Accepted
**Date:** 2026-06-04

## Context
AI workflows are notoriously complex and can quickly pollute a codebase. SpotiGram relies heavily on AI for Mood Scanning, Recommendations, and AI DJ features.

## Decision
LangChain and LangGraph libraries are **strictly restricted** to the `ai-assistant-service`.
Other AI services (`emotion-service`, `embedding-service`) must use direct API calls or lightweight libraries (e.g., `textblob`, `sentence-transformers`).

## Consequences
- **Pros:** Prevents LangChain's heavy abstraction logic from leaking into standard CRUD or pipeline services. Keeps `emotion` and `embedding` services stateless and extremely fast.
- **Cons:** We might have to re-implement minor prompt-handling logic if other services ever require it.
