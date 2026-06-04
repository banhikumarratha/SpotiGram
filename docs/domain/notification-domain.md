# Notification Domain Specification

## 1. Domain Overview
The Notification Domain handles the delivery of asynchronous alerts (likes, follows, AI suggestions) to users across multiple channels (in-app, push, email).

## 2. Aggregates & Entities
- **Aggregate Root:** `NotificationBox`
- **Entities:** `Notification`

## 3. Business Rules

### Lifecycle
- **Created:** Triggered by a domain event (e.g., `UserFollowedEvent`).
- **Queued:** Placed in Redis/Kafka for delivery.
- **Delivered:** Successfully sent to the client (or stored for in-app fetch).
- **Read:** User has explicitly acknowledged the notification.

### Rules
- **Deduplication:** Multiple likes on the same post within 1 hour by different users are aggregated ("User A and 3 others liked your post").
- **Rate Limits:** Max 5 push notifications per user per hour.
- **Failure Handling & Retries:** If push delivery fails (e.g., APNS down), retry with exponential backoff up to 3 times, then drop.

## 4. Domain Events
- `NotificationQueuedEvent(notification_id, user_id)`
- `NotificationDeliveredEvent(notification_id)`
- `NotificationReadEvent(notification_id)`

## 5. Testability Requirements
- **Unit:** Test the deduplication aggregation logic.
- **Integration:** Mock APNS/FCM endpoints to test the retry strategy.
