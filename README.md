# Spotigram

Instagram for Music Lovers.

## Architecture Overview
Spotigram uses a Hexagonal Architecture (Ports and Adapters) combined with Domain-Driven Design and Event-Driven architecture principles.
For a detailed view, see [Architecture Overview](docs/architecture_overview.md).

## Quick Start
```bash
make up
```

## Structure
- `apps/` - Frontend applications (Streamlit)
- `services/` - Independent backend microservices
- `packages/` - Shared libraries, configuration, and contracts
- `docs/` - Product requirements and engineering standards
