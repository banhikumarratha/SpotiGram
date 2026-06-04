import requests
import os
from typing import Dict, Any, Optional
import streamlit as st

class ApiClient:
    def __init__(self):
        # We assume UI is running in docker-compose network alongside these services
        self.user_svc = os.getenv("USER_SERVICE_URL", "http://user-service:8000")
        self.social_svc = os.getenv("SOCIAL_SERVICE_URL", "http://social-service:8001")
        self.ai_svc = os.getenv("AI_SERVICE_URL", "http://ai-assistant-service:8003")
        self.emotion_svc = os.getenv("EMOTION_SERVICE_URL", "http://emotion-service:8005")

    def _get(self, url: str) -> Optional[Dict[str, Any]]:
        try:
            resp = requests.get(url, timeout=5)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            st.error(f"API Request Failed: {e}")
            return None

    def _post(self, url: str, json_data: dict) -> Optional[Dict[str, Any]]:
        try:
            resp = requests.post(url, json=json_data, timeout=5)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            st.error(f"API Request Failed: {e}")
            return None

    def get_feed(self, limit=20, offset=0):
        return self._get(f"{self.social_svc}/api/v1/posts?limit={limit}&offset={offset}")
        
    def create_post(self, user_id: str, title: str, artist: str, caption: str, mood: str):
        payload = {
            "user_id": user_id,
            "track": {"spotify_id": "dummy", "title": title, "artist": artist, "duration_ms": 180000},
            "caption": caption,
            "mood": mood
        }
        return self._post(f"{self.social_svc}/api/v1/posts", payload)

    def analyze_emotion(self, text: str):
        return self._post(f"{self.emotion_svc}/api/v1/emotion/analyze", {"text": text})

    def get_ai_recommendations(self, mood: str):
        return self._get(f"{self.ai_svc}/api/v1/ai/recommendations?mood={mood}")

api_client = ApiClient()
