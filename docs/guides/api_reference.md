# API Reference

All endpoints are accessed through the **API Gateway** at `http://localhost:8000`. Authenticated endpoints require a `Bearer` token in the `Authorization` header.

---

## Auth (`/api/v1/auth`)

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/api/v1/auth/register` | No | Register a new user |
| POST | `/api/v1/auth/login` | No | Login and receive JWT |
| POST | `/api/v1/auth/logout` | Yes | Invalidate session |
| POST | `/api/v1/auth/refresh` | Yes | Rotate access token |
| POST | `/api/v1/auth/reset-password` | No | Request password reset |

### `POST /api/v1/auth/register`
```json
// Request
{ "email": "user@example.com", "password": "secret", "display_name": "Alice" }
// Response 200
{ "user_id": "uuid", "email": "user@example.com" }
```

### `POST /api/v1/auth/login`
```json
// Request
{ "email": "user@example.com", "password": "secret" }
// Response 200
{ "access_token": "jwt...", "token_type": "bearer" }
```

---

## Users (`/api/v1/users`)

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/{user_id}/follow` | Yes | Follow a user |
| DELETE | `/{user_id}/follow/{followed_id}` | Yes | Unfollow a user |
| POST | `/{user_id}/block` | Yes | Block a user |
| POST | `/{user_id}/mute` | Yes | Mute a user |
| POST | `/{user_id}/report` | Yes | Report a user |
| PUT | `/{user_id}/profile` | Yes | Update profile |

### `POST /{user_id}/follow`
```json
// Request
{ "followed_id": "target-user-uuid" }
// Response 200
{ "status": "success", "follower": "...", "followed": "..." }
```

---

## Music (`/api/v1/music`)

| Method | Path | Auth | Description |
|---|---|---|---|
| GET | `/search?q=...&type=track` | Yes | Search music catalog |
| GET | `/tracks/{track_id}` | Yes | Get track details |
| POST | `/playback` | Yes | Register playback event |
| GET | `/spotify/auth/url` | Yes | Get Spotify OAuth URL |
| POST | `/spotify/auth/refresh` | Yes | Refresh Spotify token |
| POST | `/playlists` | Yes | Create playlist |
| POST | `/playlists/import` | Yes | Import Spotify playlist |
| PUT | `/tracks/{track_id}/save` | Yes | Save track to library |
| PUT | `/artists/{artist_id}/follow` | Yes | Follow an artist |
| GET | `/fallback/musicbrainz/{track_id}` | Yes | MusicBrainz fallback |
| GET | `/fallback/lastfm/{track_id}` | Yes | Last.fm fallback |

---

## Recommendations (`/api/v1/recommendations`)

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/mood-scan` | Yes | Analyze webcam image for mood |
| GET | `/feed?mood=happy&limit=20` | Yes | Get recommendation feed |
| GET | `/similar-users` | Yes | Find users with similar DNA |
| GET | `/music-dna` | Yes | Get user's Music DNA |
| POST | `/feedback` | Yes | Submit interaction feedback |
| POST | `/mood-corrections` | Yes | Correct detected mood |
| GET | `/mood-history` | Yes | Get mood scan history |
| GET | `/music-dna/snapshots` | Yes | Get DNA timeline snapshots |

**Note**: Recommendation endpoints use `X-User-ID` header for user identification.

### `POST /mood-scan`
```json
// Request
{ "image_b64": "base64-encoded-jpeg" }
// Response 200
{ "user_id": "...", "mood": "happy", "confidence": 0.87, "detected_at": "..." }
// Response 422 (confidence < 0.6)
{ "detail": "Mood detection confidence too low. Please retake." }
```

---

## AI Assistant (`/api/v1/ai`)

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/chat` | Yes | Single-turn chat with memory |
| POST | `/stream` | Yes | Streaming SSE chat |
| POST | `/dj` | Yes | AI DJ session interaction |
| POST | `/playlist` | Yes | Generate themed playlist |
| POST | `/explain` | Yes | Explain a recommendation |

### `POST /dj`
```json
// Request
{ "session_id": "optional", "message": "Play something chill", "mood": "calm" }
// Response 200
{ "session_id": "...", "response": "..." }
```

### `POST /playlist`
```json
// Request
{ "theme": "90s Road Trip", "mood": "energetic" }
// Response 200
{ "name": "...", "description": "...", "reasoning": "...", "track_queries": [...] }
```

---

## Analytics (`/api/v1/analytics`)

| Method | Path | Auth | Description |
|---|---|---|---|
| GET | `/listening-stats?days=30` | Yes | Listening statistics |
| GET | `/mood-trends?days=30` | Yes | Mood trend analysis |
| GET | `/personality` | Yes | Music personality traits |
| GET | `/year-in-review?year=2025` | Yes | Year in Review (Wrapped) |

**Note**: Analytics endpoints use `X-User-ID` header.

---

## Observability (All Services)

| Method | Path | Description |
|---|---|---|
| GET | `/health` | Liveness probe |
| GET | `/ready` | Readiness probe |
| GET | `/metrics` | Prometheus metrics |

---

## Error Format (RFC 7807)

All errors follow Problem Details format:
```json
{
  "type": "https://spotigram.ai/errors/not-found",
  "title": "Resource Not Found",
  "status": 404,
  "detail": "User with ID xyz not found",
  "instance": "/api/v1/users/xyz"
}
```
