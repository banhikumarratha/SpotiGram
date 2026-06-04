import streamlit as st

st.title("Profile 👤")

if st.session_state.get("user_id"):
    st.write(f"Welcome to your profile, **@{st.session_state['user_id']}**!")
    st.info("Here you will see your posts and listening history.")
else:
    st.warning("Please login to view your profile.")
