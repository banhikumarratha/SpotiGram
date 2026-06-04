# Architecture Overview

SpotiGram is designed around Domain Driven Design (DDD) and Hexagonal Architecture principles.

## Core Principles
1. **Hexagonal Architecture (Ports and Adapters):** Core domain logic is isolated. External dependencies (Databases, Message Brokers, HTTP Clients) interact with the core through defined interfaces (Ports).
2. **Domain-Driven Design (DDD):** The system is divided into Bounded Contexts.
3. **Database per Service:** No service may access another service's database directly. Data sharing must happen via REST APIs or Kafka events.
4. **Async-First:** Processes that don't need to be strictly synchronous should be decoupled via Kafka events.
5. **API-First Development:** Contracts (OpenAPI/REST) are defined first. All APIs are versioned (e.g., `/api/v1/...`).
6. **Event-Driven:** Business domains broadcast state changes using versioned Kafka events.

## System Topology
- **API Services (FastAPI):** Handle business logic and expose REST endpoints.
- **UI Service (Streamlit):** Web interface interacting with API services.
- **Shared Packages (`packages/shared`):** Reusable utilities, logging configuration, and metric exporters.

## Reliability and Resilience
- Services must implement retries, timeouts, and idempotency.
- Kafka publishing must utilize the outbox pattern where transactional consistency is required.
