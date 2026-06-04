from langchain.tools import tool
import requests

@tool
def fetch_user_history(user_id: str) -> str:
    """Fetches the listening history of a user from the Social Service."""
    # Mocking HTTP call to social service feed
    return "User has recently listened to a lot of upbeat pop music."

@tool
def search_spotify_track(query: str) -> str:
    """Searches for a track on Spotify."""
    # Mocking HTTP call to music service
    return f"Found track matching '{query}': ID 12345, Vibe: Happy"
