import streamlit as st
import requests
import os

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(page_title="SpotiGram Template", page_icon="🎵")

st.title("SpotiGram UI Template")
st.write("This is a template for the SpotiGram UI.")

if st.button("Check API Health"):
    try:
        response = requests.get(f"{API_URL}/health")
        if response.status_code == 200:
            st.success(f"API is Healthy! Response: {response.json()}")
        else:
            st.error(f"API Health Check Failed. Status Code: {response.status_code}")
    except Exception as e:
        st.error(f"Failed to connect to API: {str(e)}")
