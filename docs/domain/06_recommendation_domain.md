# Recommendation Domain Specification

## 1. Overview
The Recommendation Domain synthesizes user activity, DNA, and social graphs to generate content discovery. Hosted in the `recommendation-service`.

## 2. Entities & Aggregates
- **Aggregate Root**: `RecommendationPool`
  - **Entity**: `CandidateItem`

## 3. Workflows
- **Candidate Generation**: Query Vector DB (Chroma) for tracks near user's `TasteVector` + Query recent friend likes.
- **Ranking**: Apply multiplier: (Similarity Score * 0.6) + (Social Proof * 0.4).
- **Explanation**: Generate a textual reason (e.g., "Because 3 friends liked this").
- **Cold Start**: Serve global trending tracks mapped to onboarding selections.
- **Inactive User Handling**: Fall back to generic "Top Hits in your top genre".
- **Feedback Loop**: Consume `TrackSkippedEvent` and `TrackPlayedEvent` to adjust future candidate generation weights.
- **Balanced Logic**: Ensure output contains 70% high-confidence familiar matches and 30% serendipitous discovery (low cosine similarity but high social proof).

## 4. State Transitions
N/A - This domain is primarily query and compute-driven (stateless pipelines).

## 5. Validations & Rules
- Do not recommend tracks the user has listened to in the last 24 hours.
- Maximum recommendation pool size is 500 candidates before pruning.

## 6. Permissions (RBAC)
- **System**: Core ML pipelines operate system-wide.

## 7. Edge Cases & Failure Behavior
- ChromaDB Down: Fallback to purely social-graph based recommendations (friend recent tracks).
- Homogenization Loop: Randomly inject 5% completely unmapped tracks to prevent the algorithm from trapping users in an echo chamber.

## 8. Domain Event List
- `RecommendationGeneratedEvent`

## 9. Test Scenarios
- **Given** a user skips 3 pop tracks in a row, **When** generating the next batch, **Then** pop track weights are temporarily penalized by 50%.
