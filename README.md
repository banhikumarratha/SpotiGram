# Spotigram

> **Instagram for Music Lovers** — A social music discovery platform powered by AI, mood detection, and Music DNA analysis.

## What Is Spotigram?

Spotigram is a microservices-based social music platform that lets users discover music through mood-based recommendations, AI DJ conversations, and social connections. It integrates with Spotify for playback and augments the experience with emotion detection, Music DNA fingerprinting, and LangChain/LangGraph-powered AI assistants.

## Architecture at a Glance

| Service | Port | Purpose |
|---|---|---|
| **API Gateway** | 8000 | Rate limiting, JWT auth, request routing |
| **User Service** | — | Auth, profiles, social graph (follow/block/mute) |
| **Music Service** | — | Spotify proxy, search, playback, metadata fallbacks |
| **Recommendation Service** | — | Mood scan, Music DNA, recommendation feed, ChromaDB |
| **AI Assistant Service** | — | AI DJ, playlist generation, RAG, LangGraph workflows |
| **Analytics Service** | — | Listening stats, mood trends, music personality |
| **Streamlit UI** | 8501 | Web frontend |

**Infrastructure**: PostgreSQL · Redis · Kafka · ChromaDB · Ollama · Prometheus · Grafana · Loki · Jaeger

## Quick Start

```bash
# 1. Clone and configure
cp .env.example .env
# Edit .env with your Spotify API credentials

# 2. Start all services
make local

# 3. Seed demo data
python scripts/seed_data.py

# 4. Open the UI
open http://localhost:8501
```

## Project Structure

```
SpotiGram/
├── apps/
│   └── streamlit-ui/         # Streamlit web frontend
├── services/
│   ├── api-gateway/          # FastAPI reverse proxy + rate limiter
│   ├── user-service/         # Auth, profiles, social graph
│   ├── music-service/        # Spotify integration + fallbacks
│   ├── recommendation-service/ # Mood, Music DNA, recommendations
│   ├── ai-assistant-service/ # AI DJ, RAG, LangChain/LangGraph
│   └── analytics-service/   # Listening analytics, personality
├── packages/
│   ├── spotigram-shared/     # Resilience, errors, middleware, Kafka base
│   ├── spotigram-contracts/  # Event schemas and API contracts
│   ├── spotigram-config/     # Shared configuration
│   └── spotigram-sdk/        # Service SDK helpers
├── tests/
│   ├── architecture/         # Automated fitness tests
│   ├── e2e/                  # End-to-end API scenarios
│   ├── load/                 # Locust load tests
│   └── smoke/                # Health probe verification
├── scripts/                  # Seed data, migration scripts
├── docs/                     # Full documentation set
├── docker-compose.dev.yml    # Local development stack
├── docker-compose.prod.yml   # Production stack
└── Makefile                  # Developer commands
```

## Makefile Commands

| Command | Description |
|---|---|
| `make local` | Start all services via Docker Compose |
| `make stop` | Stop all services |
| `make restart` | Restart all services |
| `make test` | Run all tests |
| `make test-unit` | Run unit tests |
| `make test-e2e` | Run end-to-end tests |
| `make test-load` | Run Locust load tests (100 users) |
| `make smoke-test` | Run health probe smoke tests |
| `make lint` | Lint with Ruff |
| `make format` | Format with Ruff |
| `make clean` | Remove caches and coverage files |

## Documentation

| Document | Path |
|---|---|
| Architecture Overview | [docs/architecture_overview.md](docs/architecture_overview.md) |
| Setup Guide | [docs/guides/setup.md](docs/guides/setup.md) |
| API Reference | [docs/guides/api_reference.md](docs/guides/api_reference.md) |
| Deployment Guide | [docs/guides/deployment.md](docs/guides/deployment.md) |
| Testing Guide | [docs/guides/testing.md](docs/guides/testing.md) |
| Troubleshooting | [docs/guides/troubleshooting.md](docs/guides/troubleshooting.md) |
| Product Spec | [docs/product/product_spec.md](docs/product/product_spec.md) |
| Business Rules | [docs/domain/business_rules.md](docs/domain/business_rules.md) |
| ADRs | [docs/adr/](docs/adr/) |

## Key Engineering Principles

- **Domain-Driven Design** — each service owns its bounded context
- **Hexagonal Architecture** — business logic depends on interfaces, not frameworks
- **Event-Driven** — Kafka-based async communication between services
- **API-First** — versioned REST APIs with structured error responses (RFC 7807)
- **AI Sandbox** — LangChain/LangGraph isolated to `ai-assistant-service`
- **Observability-First** — Prometheus metrics, structured logging, OpenTelemetry traces

## License

Private — all rights reserved.
