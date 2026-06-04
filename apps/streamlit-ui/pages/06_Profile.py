import streamlit as st
from components.navigation import render_sidebar
from utils.state import is_authenticated

st.set_page_config(page_title="Profile - Spotigram", page_icon="👤")

if not is_authenticated():
    st.switch_page("app.py")

render_sidebar()

st.title("Your Profile")

st.write(f"**Email:** {st.session_state.get('user_email')}")
st.write(f"**User ID:** {st.session_state.get('user_id')}")

st.subheader("Spotify Connection")
if st.session_state.get("spotify_connected"):
    st.success("✅ Connected to Spotify")
else:
    st.warning("❌ Not connected to Spotify")
    if st.button("Connect Now"):
        st.switch_page("pages/08_Settings.py")
