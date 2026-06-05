# Local Development Guide

## Running Individual Services

Each service can be run independently for focused development:

```bash
cd services/user-service
pip install -r requirements.txt -r requirements-dev.txt
uvicorn main:app --reload --port 8002
```

## Service Ports (when running individually)

| Service | Suggested Port |
|---|---|
| API Gateway | 8000 |
| User Service | 8002 |
| Music Service | 8003 |
| Recommendation Service | 8004 |
| AI Assistant Service | 8005 |
| Analytics Service | 8006 |
| Streamlit UI | 8501 |

## Running Tests Locally

```bash
# All tests
make test

# Only unit tests (includes per-service tests)
make test-unit

# Architecture fitness tests
pytest tests/architecture/

# Smoke tests (requires services running)
make smoke-test
```

## Running a Single Service's Tests

```bash
cd services/user-service
pytest
```

## Adding a New Feature

1. **Domain first**: Define models in `domain/models.py` as pure dataclasses.
2. **Application layer**: Create the use case in `application/`.
3. **API layer**: Add the endpoint in `api/v1/router.py`.
4. **Infrastructure**: Implement adapters in `infrastructure/`.
5. **Tests**: Add tests in the service's `tests/` directory.
6. **Event contract**: If emitting Kafka events, add the schema to `packages/spotigram-contracts`.

## Code Quality

```bash
make lint      # ruff check .
make format    # ruff format .
```

## Seeding Data

```bash
python scripts/seed_data.py
```

Creates demo user `demo@spotigram.ai` with password `demopassword`.
