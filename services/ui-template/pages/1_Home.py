import streamlit as st
from api.client import api_client
from components.ui import post_card, loading_state

st.title("Home Feed 🏠")

if st.session_state.get("user_id"):
    st.write("Here is your personalized social feed:")
    feed = api_client.get_feed()
    if feed:
        for post in feed:
            post_card(post)
    else:
        st.info("No posts found in your feed.")
else:
    st.warning("Please login to view your home feed.")
