# ADR 001: Hexagonal Architecture

**Status:** Accepted
**Date:** 2026-06-04

## Context
We need a maintainable, testable architectural pattern for the microservices in SpotiGram. Traditional layered architectures often lead to tight coupling between business logic and infrastructure (databases, HTTP clients).

## Decision
We will adopt the **Hexagonal Architecture** (Ports and Adapters).
- `domain/`: Core business logic and entities. No external dependencies.
- `application/`: Service layer coordinating domain logic.
- `infrastructure/`: Adapters for Postgres, Kafka, Redis.
- `api/`: Primary driving adapters (FastAPI routes).

## Consequences
- **Pros:** High testability (can mock repositories easily), clear separation of concerns, ability to swap infrastructure without changing business logic.
- **Cons:** Boilerplate overhead for simple CRUD operations.
