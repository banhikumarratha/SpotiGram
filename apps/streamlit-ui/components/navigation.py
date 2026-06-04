import streamlit as st
from utils.state import logout

def render_sidebar():
    with st.sidebar:
        st.title("🎵 Spotigram")
        
        if st.session_state.get("user_email"):
            st.write(f"Hello, **{st.session_state['user_email']}**!")
            
        st.divider()
        
        st.page_link("pages/01_Home.py", label="Home", icon="🏠")
        st.page_link("pages/02_Discover.py", label="Discover", icon="🔍")
        st.page_link("pages/03_Mood_Scanner.py", label="Mood Scanner", icon="📸")
        st.page_link("pages/04_Recommendations.py", label="Recommendations", icon="🎧")
        st.page_link("pages/05_AI_DJ.py", label="AI DJ", icon="🤖")
        st.page_link("pages/06_Profile.py", label="Profile", icon="👤")
        st.page_link("pages/07_Analytics.py", label="Analytics", icon="📈")
        st.page_link("pages/08_Settings.py", label="Settings", icon="⚙️")
        
        st.divider()
        if st.button("Logout", use_container_width=True):
            logout()
            st.rerun()
