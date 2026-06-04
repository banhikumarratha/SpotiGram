# Analytics Domain Specification

## 1. Overview
The Analytics Domain aggregates telemetry for both platform health and user-facing "Year in Review" features. Hosted in the `analytics-service`.

## 2. Entities & Aggregates
- **Aggregate Root**: `UserMetrics`
  - **Value Object**: `ListeningStats`

## 3. Workflows
- **Telemetry Ingestion**: Consume `TrackPlayedEvent` -> Increment time/count in fast TSDB.
- **Mood Analytics**: Aggregate `MoodScannedEvent` -> Generate weekly mood pie chart.
- **Music Personality**: Periodically snapshot `TasteProfile` -> Assign persona (e.g., "The Explorer").
- **Year-in-Review**: Batch job runs Dec 1st -> Compiles 12 months of aggregates into static JSON payload.

## 4. State Transitions
N/A

## 5. Validations & Rules
- Telemetry payloads must contain valid UserIDs.

## 6. Permissions (RBAC)
- **System**: Internal aggregation only.
- **User**: Can only read their own calculated metrics.

## 7. Edge Cases & Failure Behavior
- **Data Loss**: Kafka compaction ensures events can be replayed if the TSDB goes down.

## 8. Domain Event List
- `YearInReviewGeneratedEvent`

## 9. Test Scenarios
- **Given** a user plays 500 hours of music, **When** the monthly cron runs, **Then** `ListeningStats` correctly reflects 30,000 minutes.
