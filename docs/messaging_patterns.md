# Messaging Patterns

## Retry Strategy
If a Kafka message processing fails due to a transient error, it should not block the main topic partition.
The consumer should publish the message to a `<topic>-retry` topic with a delay/backoff metadata header, and acknowledge the original message.

## Dead-Letter Queue (DLQ)
If a message fails processing after all retries are exhausted (e.g., non-transient error like schema validation failure), it should be sent to a `<topic>-dlq` topic.
DLQ topics should have alerts configured in Grafana for manual intervention.
