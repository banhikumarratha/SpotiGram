# Local Infrastructure Setup

This document describes how to boot, configure, and troubleshoot the Spotigram microservices locally using Docker Compose.

## Startup Order & Service Dependencies

Docker Compose natively handles the startup order via `depends_on`. 
The physical boot order is:

1. **Base Infrastructure**: `postgres`, `redis`, `kafka`, `chromadb`, `ollama`
2. **Observability Stack**: `otel-collector`, `jaeger`, `prometheus`
3. **Init Containers**: `kafka-init` (waits for Kafka, creates topics)
4. **Backend Services**: `user-service`, `music-service`, `recommendation-service`, `ai-assistant-service`, `analytics-service` (Wait for DBs + Kafka)
5. **Gateway**: `api-gateway` (Waits for Redis, Kafka)
6. **Frontend**: `streamlit-ui` (Waits for Gateway)

## How to Start

Run the following command in the root of the repository:
```bash
make up
# or directly:
docker-compose -f docker-compose.dev.yml up --build
```

## Secret & Config Loading Strategy

- By default, services load configuration via `spotigram-config` which reads from the environment.
- In Docker Compose, the `.env` file at the repository root is automatically injected into all containers.
- *Best Practice*: Never commit real secrets. Use `.env.example` as a template and create a local `.env` file.

## Kafka Configuration & Topics

The `kafka-init` container automatically provisions the required domain topics on startup:
- `user.events.v1`
- `music.events.v1`
- `outbox.events`
- `spotigram.dlq`
- `spotigram.retry`

## Local Troubleshooting Notes

### 1. Kafka Connection Refused
Ensure that you are referencing `kafka:9092` inside the Docker network. If connecting from your host machine (e.g. using a local python script), map `localhost:9092` carefully as per the advertised listeners.

### 2. Ollama Missing Models
The Ollama container starts empty. To use the AI DJ locally, you must pull a model.
Exec into the container and pull:
```bash
docker exec -it spotigram-ollama-1 ollama run llama2
```

### 3. Hot-Reloading Not Working
The `docker-compose.dev.yml` uses host volumes (`./services/api-gateway:/app`). Ensure that your Docker Desktop has file sharing permissions enabled for the `SpotiGram` directory.

### 4. Database Initialization
Postgres uses a custom initialization pattern. If you change database schemas, you may need to drop the volume:
```bash
docker-compose down -v
```
