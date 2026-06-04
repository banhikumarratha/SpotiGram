# Spotigram Streamlit UI

The primary user interface for Spotigram, built with [Streamlit](https://streamlit.io/).

## Features
- **API First**: The UI abstracts backend microservices through dedicated API clients (`auth_api.py`, `spotify_api.py`, etc.).
- **Spotify Web Playback SDK**: Allows users to play music directly within the browser (Requires Spotify Premium).
- **AI DJ Chat**: Interactive chat interface connecting to the AI Assistant Service.
- **Mood Scanner**: Upload audio or enter text to detect mood.
- **Dashboards**: Integrated Plotly visualizations mapping user listening habits.

## Local Development

### Requirements
- Python 3.13+
- Backend microservices running

### Installation

```bash
uv pip install -r requirements.txt
```

### Running the App

```bash
streamlit run app.py
```

### Configuration
Update the `.env` file or export the following variables to route traffic to the respective backend microservices:

- `AUTH_SERVICE_URL` (default: http://localhost:8001)
- `SPOTIFY_SERVICE_URL` (default: http://localhost:8002)
- `MOOD_SERVICE_URL` (default: http://localhost:8003)
- `AI_SERVICE_URL` (default: http://localhost:8004)
- `ANALYTICS_SERVICE_URL` (default: http://localhost:8005)

## Architecture Details

- **`app.py`**: Handles initial routing and session setup. It acts as an authentication gate.
- **`components/`**: Reusable parts of the application (e.g., Auth Forms, Spotify Player HTML injections, Sidebars).
- **`pages/`**: The standard multi-page application structure for Streamlit UI flows.
- **`utils/state.py`**: Abstracted logic to safely manage `st.session_state` mutations across pages.
