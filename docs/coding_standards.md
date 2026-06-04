# Coding Standards

## General
- **Async-First Programming**: Use async IO for all external communications.
- **Contract-First Communication**: Define schemas (e.g. Pydantic) before implementing logic.
- **Backward Compatibility**: Changes to APIs and events must be backward compatible.
- **Observability-First Development**: All critical paths must be logged, and metrics captured.
- **Feature Flag Driven Development**: Use feature flags for new functionality.

## Python Specifics
- Use Type Hints for all function signatures and variables.
- Write unit tests for all domain logic.
- Code should be modular, testable, and maintainable.
