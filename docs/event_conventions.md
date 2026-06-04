# Event Conventions

## Naming Conventions
Kafka topics should be named using the pattern: `{domain}.{entity}.{version}`.
Example: `social.post.v1`, `user.profile.v1`.

Events themselves should follow a standard envelope structure:
```json
{
  "event_id": "uuid",
  "correlation_id": "uuid",
  "timestamp": "iso8601",
  "event_type": "EntityActioned",
  "version": "1.0",
  "payload": {}
}
```

## Versioning
Changes to event payload schemas must be backward compatible (e.g., adding optional fields).
If a breaking change is required, a new topic version (e.g., `v2`) must be created, and producers must publish to both temporarily during migration.
