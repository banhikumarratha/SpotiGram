# Troubleshooting Guide

## Common Issues

### 1. `Connection refused` on smoke tests

**Symptom**: `httpx.ConnectError: [Errno 61] Connection refused`

**Cause**: Services are not running. Smoke tests and E2E tests require the Docker Compose stack.

**Fix**:
```bash
make local
# Wait ~30 seconds for all services to boot
make smoke-test
```

### 2. Kafka topics not created

**Symptom**: Services fail to produce/consume messages.

**Cause**: The `kafka-init` container runs asynchronously and may not have completed yet.

**Fix**: Wait 15–30 seconds after `make local`, or manually create topics:
```bash
docker exec -it spotigram-kafka-1 kafka-topics.sh --create --bootstrap-server localhost:9092 --topic user.events.v1
```

### 3. Python 3.13 build errors with pydantic

**Symptom**: `TypeError: ForwardRef._evaluate() missing 1 required keyword-only argument`

**Cause**: Older `pydantic-core` builds are incompatible with Python 3.13.

**Fix**: Ensure `pydantic>=2.9.0` in `requirements.txt`.

### 4. Ollama model not available

**Symptom**: AI DJ returns 500 errors.

**Cause**: Ollama container is running but no model has been pulled yet.

**Fix**:
```bash
docker exec -it spotigram-ollama-1 ollama pull llama3
```

### 5. ChromaDB ephemeral mode issues

**Symptom**: Recommendations disappear after restart.

**Cause**: ChromaDB is running in ephemeral mode (in-memory).

**Fix**: Set `CHROMA_EPHEMERAL=false` and ensure the Docker volume `chromadata` is mounted.

### 6. JWT token expired or invalid

**Symptom**: 401 errors on API calls.

**Cause**: Token has expired (default 60 minutes) or `JWT_SECRET` mismatch between services.

**Fix**: Re-login to get a new token, and ensure all services share the same `JWT_SECRET` env var.

### 7. Spotify playback requires Premium

**Symptom**: Web Playback SDK shows "Premium required" error.

**Cause**: Spotify Web Playback SDK only works with Spotify Premium accounts.

**Fix**: Use a Premium account for playback testing, or test search/metadata features only.

### 8. Port conflicts

**Symptom**: `Bind: address already in use`

**Fix**:
```bash
make stop
# Check for lingering processes
lsof -i :8000
kill -9 <PID>
make local
```

## Checking Service Health

```bash
# All services at once
curl http://localhost:8000/health
curl http://localhost:8000/ready

# Individual service (from inside Docker network)
docker exec -it spotigram-user-service-1 curl http://localhost:8000/health
```

## Viewing Logs

```bash
# All services
docker compose -f docker-compose.dev.yml logs -f

# Specific service
docker compose -f docker-compose.dev.yml logs -f user-service
```

## Monitoring Dashboards

| Tool | URL | Credentials |
|---|---|---|
| Grafana | http://localhost:3000 | admin / admin |
| Prometheus | http://localhost:9090 | — |
| Jaeger | http://localhost:16686 | — |
