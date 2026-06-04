import pytest
from unittest.mock import patch
from api.client import APIClient
import streamlit as st

@pytest.fixture
def mock_session_state():
    with patch.dict("streamlit.session_state", {"access_token": "mock-token", "user_id": "u123"}):
        yield

def test_api_client_headers(mock_session_state):
    client = APIClient("http://mock-service")
    headers = client._get_headers()
    
    assert headers["Authorization"] == "Bearer mock-token"
    assert headers["X-User-ID"] == "u123"
    assert headers["Content-Type"] == "application/json"

def test_api_client_no_auth():
    with patch.dict("streamlit.session_state", {}, clear=True):
        client = APIClient("http://mock-service")
        headers = client._get_headers()
        
        assert "Authorization" not in headers
        assert "X-User-ID" not in headers
