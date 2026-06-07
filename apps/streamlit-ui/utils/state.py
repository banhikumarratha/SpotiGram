import streamlit as st

def init_session_state():
    """Initialize default session state variables if they don't exist."""
    defaults = {
        "access_token": None,
        "refresh_token": None,
        "user_id": None,
        "user_email": None,
        "display_name": None,
        "spotify_connected": False,
        "spotify_access_token": None,
        "current_theme": "dark",
        "messages": [], # AI DJ chat history
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def is_authenticated() -> bool:
    return st.session_state.get("access_token") is not None

def logout():
    st.session_state["access_token"] = None
    st.session_state["refresh_token"] = None
    st.session_state["user_id"] = None
    st.session_state["user_email"] = None
    st.session_state["display_name"] = None
    st.session_state["spotify_connected"] = False
    st.session_state["spotify_access_token"] = None
    st.session_state["messages"] = []
