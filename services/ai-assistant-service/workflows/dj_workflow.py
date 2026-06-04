"""
AI DJ LangGraph workflow.
State machine with 4 nodes:
  gather_context → analyze_mood → generate_transition → format_response

Uses LangGraph's StateGraph to manage multi-step reasoning with
persistent state across DJ session turns.
"""
from typing import TypedDict, Optional, List
from langgraph.graph import StateGraph, END

from domain.models import UserContext, AIResponse
from domain.ports import AIProviderPort
from infrastructure.prompt_loader import get_system_prompt, render_user_prompt


# ── LangGraph state definition ──────────────────────────────────────────────

class DJState(TypedDict):
    user_message: str
    context_str: str
    current_track: str
    mood: str
    analysis: str
    response: str
    provider: object  # AIProviderPort — not typed strictly to avoid pydantic issues


# ── Graph nodes ──────────────────────────────────────────────────────────────

async def gather_context_node(state: DJState) -> DJState:
    """Enrich state with user context string (already passed in)."""
    return state  # Context pre-loaded by DJService


async def analyze_mood_node(state: DJState) -> DJState:
    """Use LLM to briefly analyze current mood and energy."""
    provider: AIProviderPort = state["provider"]
    prompt = (
        f"In one sentence, describe the musical energy for mood '{state['mood']}'. "
        f"Current track: '{state['current_track']}'."
    )
    response = await provider.complete(prompt=prompt, temperature=0.4, max_tokens=60)
    return {**state, "analysis": response.content}


async def generate_transition_node(state: DJState) -> DJState:
    """Generate the full DJ transition suggestion."""
    provider: AIProviderPort = state["provider"]
    system = get_system_prompt("dj")
    user_prompt = render_user_prompt(
        "dj",
        context=state["context_str"],
        current_track=state["current_track"],
        mood=f"{state['mood']} — {state['analysis']}",
        user_message=state["user_message"],
    )
    response = await provider.complete(prompt=user_prompt, system=system, temperature=0.8)
    return {**state, "response": response.content}


async def format_response_node(state: DJState) -> DJState:
    """Final formatting pass — ensure response is clean."""
    return state  # Could add post-processing here


# ── Build the graph ───────────────────────────────────────────────────────────

def build_dj_graph() -> StateGraph:
    graph = StateGraph(DJState)
    graph.add_node("gather_context", gather_context_node)
    graph.add_node("analyze_mood", analyze_mood_node)
    graph.add_node("generate_transition", generate_transition_node)
    graph.add_node("format_response", format_response_node)

    graph.set_entry_point("gather_context")
    graph.add_edge("gather_context", "analyze_mood")
    graph.add_edge("analyze_mood", "generate_transition")
    graph.add_edge("generate_transition", "format_response")
    graph.add_edge("format_response", END)

    return graph.compile()


# Module-level compiled graph (singleton)
_dj_graph = None


def get_dj_graph():
    global _dj_graph
    if _dj_graph is None:
        _dj_graph = build_dj_graph()
    return _dj_graph


async def run_dj_workflow(
    user_message: str,
    context_str: str,
    current_track: str,
    mood: str,
    provider: AIProviderPort,
) -> str:
    """Entry point — run the full AI DJ LangGraph workflow."""
    graph = get_dj_graph()
    initial_state: DJState = {
        "user_message": user_message,
        "context_str": context_str,
        "current_track": current_track or "Nothing playing yet",
        "mood": mood or "neutral",
        "analysis": "",
        "response": "",
        "provider": provider,
    }
    final_state = await graph.ainvoke(initial_state)
    return final_state.get("response", "")
