# Feed Domain Specification

## 1. Overview
The Feed Domain aggregates social activity, system recommendations, and trending items into a cohesive infinite scroll.

## 2. Entities & Aggregates
- **Aggregate Root**: `Timeline`
  - **Entity**: `FeedPage`

## 3. Workflows
- **Feed Ranking**: Fetch friend posts (60%) + recommendations (30%) + trending (10%) -> Sort by EdgeRank formula.
- **Recommendations Insertion**: Inject `FeedItemType.RECOMMENDATION` every Nth slot in the UI.
- **Pagination**: Client requests cursor -> DB queries records older than cursor timestamp -> Returns next cursor.
- **Cache Invalidation**: On new friend post -> Invalidate specific user's Redis timeline cache.

## 4. State Transitions
N/A - Read-heavy projection domain.

## 5. Validations & Rules
- Do not show posts from blocked users.
- Muted users' posts appear in timeline but are deprioritized by 90%.

## 6. Permissions (RBAC)
- **User**: Can view own timeline.

## 7. Edge Cases & Failure Behavior
- **Cache Miss**: Fallback to expensive DB query with a hard limit of 50 items to protect DB load.
- **Empty Feed**: If user has no friends, fill 100% with recommendations.

## 8. Domain Event List
- `FeedViewedEvent`

## 9. Test Scenarios
- **Given** a user has 0 friends, **When** they request their feed, **Then** they receive 100% `RECOMMENDATION` type items.
