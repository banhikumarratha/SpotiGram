# Security Domain Specification

## 1. Overview
The Security Domain handles cross-cutting concerns like AuthZ, API gateways, and secret management. Hosted primarily in `api-gateway`.

## 2. Entities & Aggregates
- **Aggregate Root**: `SecurityPolicy`

## 3. Workflows
- **Authentication**: Gateway validates JWT signature via public JWKS.
- **Authorization**: Gateway checks `roles` claim in JWT against endpoint requirements.
- **Rate Limiting**: Redis-based sliding window (100 req/min per user).
- **Audit Logging**: Write administrative actions (e.g., `UserSuspendedEvent`) to an append-only audit log.
- **Secret Handling**: Rotate application secrets (Spotify OAuth, JWT keys) without downtime using HashiCorp Vault or AWS Secrets Manager.

## 4. State Transitions
N/A

## 5. Validations & Rules
- All requests must have a correlation ID.
- Missing JWT immediately returns 401.
- Expired JWT immediately returns 401.

## 6. Permissions (RBAC)
- **SuperAdmin**: Full system access.

## 7. Edge Cases & Failure Behavior
- **Brute Force**: 5 failed logins locks the IP for 15 minutes.
- **Redis Down**: Rate limiting fails open (allows traffic) but logs a critical warning.

## 8. Domain Event List
- `RateLimitExceededEvent`
- `SecurityAnomalyDetectedEvent`

## 9. Test Scenarios
- **Given** an IP exceeds 100 req/min, **When** a new request arrives, **Then** the gateway returns `429 Too Many Requests`.
