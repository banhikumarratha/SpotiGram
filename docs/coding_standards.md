# Coding Standards

1. **API First**: Define OpenAPI specs before implementation.
2. **Hexagonal Architecture**: Isolate domain logic from ports (HTTP/Events) and adapters (DB/External APIs).
3. **Observability First**: All errors must be logged. Use the shared logger.
4. **Resilience**: Expect failure. Provide fallbacks (e.g., MusicBrainz for Spotify metadata).
5. **No Cross-DB Queries**: Services may only interact via APIs or Events.
6. **Tests Required**: Every PR must include tests.
