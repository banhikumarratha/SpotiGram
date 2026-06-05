# Testing Guide

## Test Taxonomy

| Test Type | Location | Command | Requires Services? |
|---|---|---|---|
| **Unit** | `services/*/tests/` | `make test-unit` | No |
| **Architecture** | `tests/architecture/` | `pytest tests/architecture/` | No |
| **Integration** | `tests/integration/` | `make test-integration` | Partial |
| **Contract** | `tests/contract/` | `make test-contract` | No |
| **E2E** | `tests/e2e/` | `make test-e2e` | Yes |
| **Smoke** | `tests/smoke/` | `make smoke-test` | Yes |
| **Load** | `tests/load/` | `make test-load` | Yes |

## Running Tests

```bash
# Everything
make test

# Unit tests only (fast, no infra needed)
make test-unit

# E2E (requires `make local` first)
make local
make test-e2e

# Load testing with Locust (100 concurrent users)
make test-load
```

## Architecture Fitness Tests

Located in `tests/architecture/test_fitness.py`. These are static analysis tests that parse the Python AST to enforce:

1. **AI Sandbox**: LangChain/LangGraph only in `ai-assistant-service`
2. **Database Isolation**: No cross-service database imports
3. **API Versioning**: Router prefixes follow `/api/v{n}/` convention
4. **Health Probes**: Every `main.py` exposes `/health`, `/ready`, `/metrics`
5. **No Hardcoded Credentials**: Scans for leaked secrets

```bash
pytest tests/architecture/test_fitness.py -v
```

## E2E Scenarios

The E2E test suite (`tests/e2e/test_scenarios.py`) validates full user journeys:

| Scenario | Flow |
|---|---|
| 1 | Signup → Login → Spotify Connect → Mood Scan → Feed Update |
| 2 | Login → Search → Play → DNA Update → Recommendation Refresh |
| 3 | AI DJ → Generate Playlist → Save Playlist |

## Load Testing

Uses Locust (`tests/load/locustfile.py`) targeting 100 concurrent users across:
- Login flow
- Feed browsing
- Spotify search
- AI DJ chat
- Analytics queries

Metrics collected: latency, throughput, error rate, p95, p99.

```bash
# Headless mode
make test-load

# UI mode
locust -f tests/load/locustfile.py
# Open http://localhost:8089
```

## Acceptance Test Report

The full acceptance test report is at `docs/testing/acceptance_test_report.md`. It covers 60+ test cases across User, Spotify, Mood, Music DNA, Recommendation, AI DJ, Analytics, Infrastructure, and Failure scenarios.

## Writing New Tests

- Place unit tests inside the owning service's `tests/` directory.
- Use `pytest` with `pytest-asyncio` for async tests.
- Mock external dependencies using `unittest.mock.AsyncMock`.
- For integration tests requiring real databases, use `testcontainers`.
