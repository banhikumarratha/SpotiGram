# ADR-003: Event-Driven Architecture with Kafka

**Date**: 2025-02-15
**Status**: Accepted

## Context
Services need to communicate state changes (user registered, track played) without tight coupling or synchronous request chains.

## Decision
Use Apache Kafka as the event bus with versioned topics:
- `user.events.v1` — User lifecycle events
- `music.events.v1` — Music interaction events
- `spotigram.dlq` — Dead Letter Queue for failed messages
- `spotigram.retry` — Retry queue

Events follow a contract-first envelope format with headers (event_id, correlation_id, idempotency_key, timestamp, version) and a payload.

## Consequences
- Services are loosely coupled via events
- Temporal decoupling — consumers process at their own pace
- Failed messages are captured in DLQ for manual inspection
- Event versioning prevents breaking changes
