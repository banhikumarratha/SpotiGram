# Service Ownership Guide

## Ownership Matrix

| Service | Bounded Context | Database | Kafka Topics | Owner Team |
|---|---|---|---|---|
| **api-gateway** | Request Routing & Security | — (uses Redis) | — | Platform |
| **user-service** | Identity & Social Graph | PostgreSQL (`users`, `profiles`, `connections`) | `user.events.v1` (producer) | Identity |
| **music-service** | Music Catalog & Playback | — | `music.events.v1` (producer) | Music |
| **recommendation-service** | Mood, Music DNA, Recommendations | ChromaDB | `music.events.v1` (consumer) | Discovery |
| **ai-assistant-service** | Conversational AI & Playlists | — (in-memory) | — | AI |
| **analytics-service** | Aggregated Insights | PostgreSQL (`daily_user_stats`) | `user.events.v1`, `music.events.v1` (consumer) | Data |
| **streamlit-ui** | Web Frontend | — | — | Frontend |

## Service Contact Points

Each service is self-contained with:
- Its own `Dockerfile`
- Its own `requirements.txt` and `requirements-dev.txt`
- Its own `pytest.ini` and `tests/` directory
- Its own `main.py` with `/health`, `/ready`, `/metrics`

## Shared Packages

| Package | Purpose | Used By |
|---|---|---|
| `spotigram-shared` | Resilience (retries, circuit breakers), error handling, Kafka DLQ base consumer, idempotency middleware, outbox pattern | All services |
| `spotigram-contracts` | Event schemas, API contracts | All services |
| `spotigram-config` | Shared configuration management | All services |
| `spotigram-sdk` | Service SDK helpers | All services |

## On-Call Responsibilities

- **Platform team** owns the API Gateway, Docker Compose, and infrastructure (Kafka, Redis, PostgreSQL).
- **Each domain team** owns their bounded context end-to-end (API → Application → Domain → Infrastructure → Tests).
- **AI team** is the sole owner of any LangChain/LangGraph code. No other team may import these libraries.
