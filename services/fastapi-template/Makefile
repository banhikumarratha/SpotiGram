.PHONY: run test lint

run:
	uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload

test:
	PYTHONPATH=. pytest tests/

lint:
	echo "Running linter..."
