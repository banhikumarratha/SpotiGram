import streamlit as st
from utils.state import logout
import jwt
from api.auth_api import AuthAPI

def render_sidebar():
    # Restore user_id from token if missing but authenticated
    if (not st.session_state.get("user_id") or st.session_state.get("user_id") == "None") and st.session_state.get("access_token"):
        try:
            decoded = jwt.decode(st.session_state["access_token"], options={"verify_signature": False})
            st.session_state["user_id"] = decoded.get("sub")
        except Exception:
            pass

    # Fetch user display name and email if missing
    user_id = st.session_state.get("user_id")
    if user_id and user_id != "None" and (not st.session_state.get("display_name") or not st.session_state.get("user_email") or st.session_state.get("user_email") == "Unknown Email"):
        try:
            auth_api = AuthAPI()
            res = auth_api.get_profile(user_id)
            if res.status_code == 200:
                data = res.json()
                st.session_state["display_name"] = data.get("display_name") or "User"
                st.session_state["user_email"] = data.get("email") or "Unknown Email"
        except Exception:
            pass

    with st.sidebar:
        st.title("🎵 Spotigram")
        
        display_name = st.session_state.get("display_name") or st.session_state.get("user_email") or "User"
        if display_name:
            st.write(f"Hello, **{display_name}**!")
            
        st.divider()
        
        st.page_link("app.py", label="Home", icon="🏠")
        st.page_link("pages/02_Discover.py", label="Discover", icon="🔍")
        st.page_link("pages/03_Mood_Scanner.py", label="Mood Scanner", icon="📸")
        st.page_link("pages/04_Recommendations.py", label="Recommendations", icon="🎧")
        st.page_link("pages/05_AI_DJ.py", label="AI DJ", icon="🤖")
        st.page_link("pages/07_Analytics.py", label="Analytics", icon="📈")
        
        st.divider()
        if st.button("Logout", use_container_width=True):
            logout()
            st.rerun()
