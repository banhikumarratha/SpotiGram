# Spotigram Workspace Rules

## Architecture
- Use FastAPI for services.
- Use Streamlit for UI.
- Use PostgreSQL, Redis, Kafka, ChromaDB, Ollama.
- LangChain and LangGraph only inside ai-assistant-service.
- No service may access another service's database.
- All APIs must be versioned.
- All Kafka events must be versioned.

## Code
- Generate only files relevant to the current phase.
- Do not regenerate the whole repo.
- Add tests with every feature.
- Keep modules small and reusable.
- Prefer clean architecture and hexagonal boundaries.

## Reliability
- Use retries, timeouts, and idempotency.
- Use health checks and readiness checks.
- Use structured logs and metrics.
- Use outbox pattern for event publishing where needed.

## Testability
- Every service must be independently testable.
- Every service must support unit, integration, and contract tests.
- The full system must support end-to-end tests.