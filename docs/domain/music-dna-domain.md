# Music DNA Domain Specification

## 1. Domain Overview
Music DNA is the evolving, foundational representation of a user's musical identity. It aggregates cross-domain signals to build a persistent profile for hyper-personalized recommendations.

## 2. Aggregates & Entities
- **Aggregate Root:** `DNAProfile`
- **Entities:** `SignalEvent`, `DNASnapshot`

## 3. Business Rules

### Inputs & Evolution
Music DNA evolves continuously based on a stream of events:
- **Songs Played:** Heavy positive signal.
- **Songs Skipped:** Negative signal if skipped within 30 seconds.
- **Songs Liked:** Massive positive signal.
- **Playlists Created:** Defines core genre affinities.
- **Moods Detected:** Correlates genres/tempos with emotional states.
- **Social Interactions:** (e.g., Liking a friend's post). Moderate positive signal for the shared track.

### Algorithmic Rules
- **Weighting Model:**
  - Like: 5.0 points
  - Full Play: 3.0 points
  - Social Interaction: 1.5 points
  - Skip: -2.0 points
- **Recency Bias:** Events in the last 7 days carry a 1.5x multiplier.
- **Decay Strategy:** Event weights decay logarithmically over 90 days. Signals older than 90 days are baked into the "Core Affinity" baseline but lose their immediate contextual weight.
- **Historical Snapshots:** A materialized `DNASnapshot` is generated weekly for analytics and rollback purposes.
- **Update Frequency:** The real-time DNA vector is updated asynchronously via Kafka streams, eventually consistent (SLA: < 2 minutes).

## 4. Domain Events
- `DNASnapshotGeneratedEvent(user_id, snapshot_id, timestamp)`
- `DNAVectorUpdatedEvent(user_id, new_vector_hash)`
- `SignificantTasteShiftDetectedEvent(user_id, from_genre, to_genre)`

## 5. Testability Requirements
- **Unit:** Test the decay formula and weighting multipliers independently.
- **Integration:** Ensure Kafka consumers correctly aggregate multiple concurrent signals without race conditions.
