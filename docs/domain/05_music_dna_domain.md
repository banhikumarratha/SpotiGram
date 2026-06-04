# Music DNA Domain Specification

## 1. Overview
The Music DNA Domain calculates and maintains complex acoustic vectors to represent a user's taste. Hosted in the `recommendation-service`.

## 2. Entities & Aggregates
- **Aggregate Root**: `TasteProfile`
  - **Value Objects**: `TasteVector` (Acousticness, Danceability, Energy, Valence, Tempo)
  - **Entity**: `TasteSnapshot`

## 3. Workflows
- **DNA Creation**: Consume initial Spotify top tracks -> Average acoustic features -> Generate baseline `TasteVector`.
- **DNA Update**: Consume `TrackPlayedEvent` -> Recalculate vector using exponential moving average (EMA).
- **Snapshots**: Run cron job monthly -> Save current vector to `TasteSnapshot` table.
- **Similarity Scoring**: Compare two `TasteVector`s using Cosine Similarity to find "Music Soulmates".

## 4. Weighting & Decay Strategy
- **Weighting Model**: High-rotation tracks carry 3x weight compared to one-off listens.
- **Recency Bias**: Tracks played in the last 7 days influence the vector 2x more than tracks played 30 days ago.
- **Decay Strategy**: Older listening events decay linearly until they fall out of the calculation window (90 days).

## 5. State Transitions
- DNA states are continuously evolving numeric vectors, rather than discrete state machine steps. (Baseline -> Evolving -> Snapshotted).

## 6. Validations & Rules
- Vector values must normalize between 0.0 and 1.0.
- Similarity scoring only runs for users with at least 50 track events to avoid false positives on cold starts.

## 7. Permissions (RBAC)
- **System**: Background workers calculate and snapshot DNA.

## 8. Edge Cases & Failure Behavior
- Cold Start: Users with 0 Spotify history prompt manual onboarding artist selection.
- Extreme outlier track (e.g., accidentally leaving white noise on overnight): Detected via frequency anomaly and excluded from DNA calculation.

## 9. Domain Event List
- `MusicDNACalculatedEvent`
- `TasteSnapshotCreatedEvent`

## 10. Test Scenarios
- **Given** User A and User B have a cosine similarity of 0.95, **When** calculating soulmates, **Then** they are flagged as `HIGH_MATCH`.
