# API Conventions

## API Versioning Strategy
All APIs must be versioned in the URL path.
Example: `/api/v1/users`, `/api/v1/posts`

## Correlation ID Format
All incoming requests should include an `X-Correlation-ID` header (UUID v4).
If missing, the API gateway or first service must generate it. It must be propagated to all downstream requests and Kafka events.

## Error Response Format
All HTTP errors must follow this structure:
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE_STRING",
    "message": "Human readable message",
    "details": {} 
  }
}
```

## Pagination Format
Paginated endpoints should use cursor-based or limit/offset pagination and return metadata:
```json
{
  "success": true,
  "data": [...],
  "pagination": {
    "total": 100,
    "limit": 20,
    "offset": 0,
    "next_cursor": "string_or_null"
  }
}
```
