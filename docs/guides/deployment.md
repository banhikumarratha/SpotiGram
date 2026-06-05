# Deployment Guide

## Environments

| Environment | Compose File | Purpose |
|---|---|---|
| Development | `docker-compose.dev.yml` | Hot-reload, all infra locally |
| Production | `docker-compose.prod.yml` | Optimized images, no dev tools |

## Development Deployment

```bash
make local     # docker compose -f docker-compose.dev.yml up -d --build
make stop      # docker compose -f docker-compose.dev.yml down
make restart   # stop + local
```

## Production Deployment

### 1. Build Images

```bash
docker compose -f docker-compose.prod.yml build
```

### 2. Configure Secrets

All secrets must be provided via environment variables. Never commit secrets to source control.

Required production environment variables:
```
JWT_SECRET=<strong-random-secret>
DATABASE_URL=postgresql://<user>:<pass>@<host>:5432/spotigram
REDIS_URL=redis://<host>:6379
KAFKA_BOOTSTRAP_SERVERS=<host>:9092
SPOTIFY_CLIENT_ID=<from-spotify-dashboard>
SPOTIFY_CLIENT_SECRET=<from-spotify-dashboard>
OLLAMA_BASE_URL=http://<ollama-host>:11434
```

### 3. Deploy

```bash
docker compose -f docker-compose.prod.yml up -d
```

### 4. Verify

```bash
curl https://your-domain.com/health
curl https://your-domain.com/ready
```

## Infrastructure Dependencies

| Component | Dev Image | Production Recommendation |
|---|---|---|
| PostgreSQL | `postgres:15-alpine` | AWS RDS / Cloud SQL |
| Redis | `redis:7-alpine` | AWS ElastiCache / Cloud Memorystore |
| Kafka | `bitnami/kafka:3.5` | AWS MSK / Confluent Cloud |
| ChromaDB | `chromadb/chroma:latest` | Self-hosted or managed |
| Ollama | `ollama/ollama:latest` | GPU-enabled VM or cloud AI endpoint |
| Prometheus | `prom/prometheus:latest` | Grafana Cloud |
| Grafana | `grafana/grafana:latest` | Grafana Cloud |
| Loki | `grafana/loki:latest` | Grafana Cloud |
| Jaeger | `jaegertracing/all-in-one:latest` | Managed tracing (Datadog, etc.) |

## Health Checks

All services expose:
- `GET /health` — Liveness probe (returns 200 if process is alive)
- `GET /ready` — Readiness probe (returns 200 if dependencies are connected)
- `GET /metrics` — Prometheus-compatible metrics endpoint
