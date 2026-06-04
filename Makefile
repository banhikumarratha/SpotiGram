.PHONY: help run-local down-local test lint

help:
	@echo "Available commands:"
	@echo "  run-local     - Start the entire SpotiGram platform locally"
	@echo "  down-local    - Stop the local platform"
	@echo "  test          - Run tests across all services"
	@echo "  lint          - Lint all code"

run-local:
	docker-compose up --build -d

down-local:
	docker-compose down

test:
	@echo "Running tests in all services..."
	make -C services/fastapi-template test
	make -C services/streamlit-template test

lint:
	@echo "Linting all code..."
	make -C services/fastapi-template lint
	make -C services/streamlit-template lint
