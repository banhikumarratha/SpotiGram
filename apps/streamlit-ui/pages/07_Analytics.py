import streamlit as st
import pandas as pd
import plotly.express as px
from components.navigation import render_sidebar
from api.analytics_api import AnalyticsAPI
from utils.state import is_authenticated

st.set_page_config(page_title="Analytics - Spotigram", page_icon="📈", layout="wide")

if not is_authenticated():
    st.switch_page("app.py")

render_sidebar()

st.title("Analytics Dashboard")

api = AnalyticsAPI()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Listening Stats (Last 30 Days)")
    try:
        res = api.get_listening_stats(days=30)
        if res.status_code == 200:
            stats = res.json()
            st.metric("Total Plays", stats.get("total_plays", 0))
            st.metric("Total Skips", stats.get("total_skips", 0))
            st.metric("Completion Rate", f"{stats.get('completion_rate', 0)*100:.1f}%")
        else:
            st.error("Failed to load listening stats.")
    except Exception as e:
        st.error(f"Error: {e}")

with col2:
    st.subheader("Music Personality")
    try:
        res = api.get_personality()
        if res.status_code == 200:
            pers = res.json()
            traits = pers.get("traits", [])
            for t in traits:
                st.write(f"- {t}")
            if not traits:
                st.write("Not enough data to determine personality.")
        else:
            st.error("Failed to load personality.")
    except Exception as e:
        st.error(f"Error: {e}")

st.divider()

st.subheader("Mood Trends")
try:
    res = api.get_mood_trends(days=30)
    if res.status_code == 200:
        trends = res.json()
        mood_counts = trends.get("mood_counts", {})
        if mood_counts:
            df = pd.DataFrame(list(mood_counts.items()), columns=['Mood', 'Count'])
            fig = px.pie(df, values='Count', names='Mood', title='Mood Distribution')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No mood data recorded in the last 30 days.")
    else:
        st.error("Failed to load mood trends.")
except Exception as e:
    st.error(f"Error: {e}")
