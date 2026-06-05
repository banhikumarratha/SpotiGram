.PHONY: test test-unit test-integration test-contract test-e2e test-load smoke-test local stop restart lint format clean

# -----------------------------------------------------------------------------
# Testing Commands
# -----------------------------------------------------------------------------

test:
	pytest tests/

test-unit:
	pytest tests/unit/ services/*/tests/ -m "not integration and not e2e"

test-integration:
	pytest tests/integration/ services/*/tests/ -m "integration"

test-contract:
	pytest tests/contract/

test-e2e:
	pytest tests/e2e/

test-load:
	locust -f tests/load/locustfile.py --headless -u 100 -r 10 --run-time 1m

smoke-test:
	pytest tests/smoke/

# -----------------------------------------------------------------------------
# Local Development
# -----------------------------------------------------------------------------

local:
	docker compose -f docker-compose.dev.yml up -d --build

stop:
	docker compose -f docker-compose.dev.yml down

restart: stop local

# -----------------------------------------------------------------------------
# Code Quality
# -----------------------------------------------------------------------------

lint:
	ruff check .

format:
	ruff format .

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	rm -rf .coverage htmlcov
