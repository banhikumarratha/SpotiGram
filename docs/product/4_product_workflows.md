# Product Workflows

## 1. Authentication & API Flow
1. **User lands on Streamlit App**.
2. **Auth Selection**: User chooses Email/Password or Spotify OAuth.
3. **Spotify Connect**: User grants permissions. Backend verifies Premium status.
4. **Token Management**: Backend stores access/refresh tokens and handles silent refreshes.
5. **Data Hydration**: API fetches top artists/tracks to generate initial Music DNA.

## 2. Music Playback Flow (Streamlit + JS)
1. **Feed Render**: Streamlit renders the UI, including a custom HTML/JS component for the Spotify player.
2. **User Action**: User clicks "Play" on a feed item.
3. **JS Execution**: The Streamlit component sends the Spotify URI to the injected JavaScript.
4. **Web Playback SDK**: JS communicates with Spotify Web API Player Endpoints to start playback on the active Web Player device.
5. **State Sync**: JS passes playback state back to Streamlit to update the UI (pause/play icons, progress bar).

## 3. Metadata Fallback Flow
1. **Track Load**: User opens a detailed track view.
2. **Spotify Query**: Backend queries Spotify API for track metadata.
3. **Fallback Check**: If specific metadata (e.g., release labels, obscure genres) is missing, backend queries MusicBrainz.
4. **Secondary Fallback**: If still missing, backend queries Last.fm.
5. **Data Merge**: Backend combines data and serves a unified JSON response to the Streamlit frontend.

## 4. Moderation Flow
1. **Action**: User reports a comment.
2. **Database**: Flag is added to the database for the specific comment ID.
3. **Visibility**: Comment is instantly hidden for the reporting user.
4. **Admin Queue**: Flagged item appears in a basic admin dashboard for review.
