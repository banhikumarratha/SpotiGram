# ADR-001: Hexagonal Architecture per Service

**Date**: 2025-01-15
**Status**: Accepted

## Context
We need a consistent internal architecture for each microservice that separates business logic from framework concerns and external integrations.

## Decision
Each service follows Hexagonal Architecture (Ports & Adapters):
- `domain/` — Pure Python dataclasses and enums, zero framework imports
- `application/` — Use cases that depend on domain interfaces
- `infrastructure/` — Driven adapters (PostgreSQL, Kafka, ChromaDB, HTTP clients)
- `api/v1/` — Driving adapters (FastAPI routers)

## Consequences
- Business logic is framework-agnostic and easily testable
- Infrastructure can be swapped without changing domain logic
- Consistent structure across all 6 services
