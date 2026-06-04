import streamlit as st
from components.navigation import render_sidebar
from components.chat_ui import render_chat_interface
from utils.state import is_authenticated

st.set_page_config(page_title="AI DJ - Spotigram", page_icon="🤖")

if not is_authenticated():
    st.switch_page("app.py")

render_sidebar()

st.title("AI DJ")
render_chat_interface()
