import streamlit as st

st.title("Settings ⚙️")
st.write("Manage your SpotiGram preferences and connected accounts.")
st.toggle("Dark Mode (System Default)", value=True, disabled=True)
st.toggle("Connect Spotify Account", value=False)
