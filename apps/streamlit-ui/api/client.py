import httpx
import streamlit as st
from typing import Optional, Dict, Any

class APIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def _get_headers(self) -> Dict[str, str]:
        headers = {"Content-Type": "application/json"}
        token = st.session_state.get("access_token")
        if token:
            headers["Authorization"] = f"Bearer {token}"

        # some services expect X-User-ID — always send it with a fallback
        user_id = st.session_state.get("user_id") or "anonymous"
        headers["X-User-ID"] = user_id

        return headers

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> httpx.Response:
        with httpx.Client(base_url=self.base_url, headers=self._get_headers(), timeout=120.0) as client:
            return client.get(endpoint, params=params)

    def post(self, endpoint: str, json: Optional[Dict[str, Any]] = None, data: Any = None, files: Any = None) -> httpx.Response:
        headers = self._get_headers()
        # If posting files, let httpx set the content-type boundary
        if files:
            headers.pop("Content-Type", None)
            
        with httpx.Client(base_url=self.base_url, headers=headers, timeout=120.0) as client:
            return client.post(endpoint, json=json, data=data, files=files)

    def put(self, endpoint: str, json: Optional[Dict[str, Any]] = None) -> httpx.Response:
        with httpx.Client(base_url=self.base_url, headers=self._get_headers(), timeout=120.0) as client:
            return client.put(endpoint, json=json)

    def delete(self, endpoint: str) -> httpx.Response:
        with httpx.Client(base_url=self.base_url, headers=self._get_headers(), timeout=120.0) as client:
            return client.delete(endpoint)
