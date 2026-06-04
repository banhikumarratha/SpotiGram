import streamlit as st

st.set_page_config(
    page_title="SpotiGram",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Authentication State
if "user_id" not in st.session_state:
    st.session_state["user_id"] = None

with st.sidebar:
    st.title("🎵 SpotiGram")
    st.markdown("---")
    
    if st.session_state["user_id"] is None:
        st.subheader("Login")
        username = st.text_input("Username")
        if st.button("Login"):
            st.session_state["user_id"] = username
            st.rerun()
    else:
        st.write(f"Logged in as **@{st.session_state['user_id']}**")
        if st.button("Logout"):
            st.session_state["user_id"] = None
            st.rerun()

st.title("Welcome to SpotiGram 🎶")
st.markdown("Navigate using the sidebar to explore your music and social feeds.")
if st.session_state["user_id"] is None:
    st.warning("Please login from the sidebar to access all features.")
