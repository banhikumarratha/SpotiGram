# Coding Standards

This project adheres to strict coding guidelines to ensure maintainability, testability, and consistency.

## Language and Style
- **Language:** Python 3.12+
- **Linter/Formatter:** Ruff and Black
- **Type Checking:** Mypy (Strict mode enabled)
- Use standard Python typing (e.g., `list[str]`, `dict[str, Any]`).

## Architecture Rules
1. **Directory Structure:** 
   Services must follow Hexagonal Architecture:
   - `domain/`: Core business models and rules (No external dependencies).
   - `application/`: Use cases/services orchestrating domain models.
   - `infrastructure/`: Database repositories, Kafka producers/consumers, external API clients.
   - `api/`: FastAPI routers and dependency injection.
2. **No Business Logic in Routers:** FastAPI routers should only handle request parsing, calling application services, and formatting responses.

## Testing
- **Unit Tests:** Must be written for all domain logic and application services.
- **Integration Tests:** Must be written for all infrastructure adapters (DBs, Kafka).
- **Framework:** Use `pytest`.
- Each PR must maintain or increase code coverage.

## API Standards
- Always version APIs (e.g., `/api/v1/resource`).
- Use Pydantic models for all request and response validation.
- Every service must expose `/health`, `/ready`, and `/metrics`.
