from typing import Dict, TypedDict
from langgraph.graph import StateGraph, END
from application.ai_provider import get_llm
from application.tools import fetch_user_history, search_spotify_track

class DJState(TypedDict):
    user_id: str
    mood: str
    history: str
    recommendation: str

def fetch_history_node(state: DJState):
    history = fetch_user_history.invoke(state["user_id"])
    return {"history": history}

def generate_recommendation_node(state: DJState):
    llm = get_llm()
    prompt = f"User {state['user_id']} likes {state['history']}. They are currently feeling {state['mood']}. Suggest a track."
    # Since Ollama invoke might fail if offline, the fallback handles it
    try:
        response = llm.invoke(prompt)
    except Exception:
        response = "[Fallback] Mock Track"
    return {"recommendation": response}

def build_ai_dj_workflow() -> StateGraph:
    workflow = StateGraph(DJState)
    
    workflow.add_node("fetch_history", fetch_history_node)
    workflow.add_node("generate_recommendation", generate_recommendation_node)
    
    workflow.set_entry_point("fetch_history")
    workflow.add_edge("fetch_history", "generate_recommendation")
    workflow.add_edge("generate_recommendation", END)
    
    return workflow.compile()
