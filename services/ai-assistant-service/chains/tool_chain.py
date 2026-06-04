"""
Tool chain — LangChain-based tool-calling orchestration.
Currently supports: search_tracks, explain_recommendation.
Tools are defined as structured functions and dispatched by the LLM.
"""
import json
import logging
from typing import Optional

from domain.models import UserContext, AIResponse, GeneratedPlaylist
from domain.ports import AIProviderPort
from infrastructure.prompt_loader import get_system_prompt, render_user_prompt

logger = logging.getLogger(__name__)


async def generate_playlist(
    theme: str,
    provider: AIProviderPort,
    context: Optional[UserContext] = None,
    mood: str = "any",
    prompt_version: str = "v1",
) -> GeneratedPlaylist:
    """
    Uses the LLM to generate a themed playlist with structured JSON output.
    The playlist prompt instructs the model to return strict JSON.
    """
    context_str = context.as_context_string() if context else "No user context."
    genres = ", ".join(context.top_genres[:5]) if context and context.top_genres else "any"

    system = get_system_prompt("playlist", prompt_version)
    user_prompt = render_user_prompt(
        "playlist",
        version=prompt_version,
        context=context_str,
        theme=theme,
        mood=mood,
        genres=genres,
    )

    response = await provider.complete(prompt=user_prompt, system=system, temperature=0.9)

    # Parse structured JSON output
    try:
        # Strip markdown code fences if present
        raw = response.content.strip()
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        data = json.loads(raw.strip())
        return GeneratedPlaylist(
            name=data.get("name", "My Playlist"),
            description=data.get("description", ""),
            track_queries=data.get("track_queries", []),
            reasoning=data.get("reasoning", ""),
            mood=mood,
        )
    except (json.JSONDecodeError, KeyError) as e:
        logger.warning("Failed to parse playlist JSON: %s — using fallback", e)
        return GeneratedPlaylist(
            name=f"Playlist for: {theme}",
            description=f"A {mood} playlist themed around: {theme}",
            track_queries=[response.content],
            reasoning="Generated without structured parsing",
            mood=mood,
        )


async def explain_recommendation(
    track_title: str,
    track_artist: str,
    signals: dict,
    provider: AIProviderPort,
    context: Optional[UserContext] = None,
    prompt_version: str = "v1",
) -> str:
    """Generate a human-readable explanation for a recommendation."""
    context_str = context.as_context_string() if context else "No user context."
    system = get_system_prompt("explain", prompt_version)
    user_prompt = render_user_prompt(
        "explain",
        version=prompt_version,
        context=context_str,
        track_title=track_title,
        track_artist=track_artist,
        signals=json.dumps(signals, indent=2),
    )
    response = await provider.complete(prompt=user_prompt, system=system, temperature=0.6)
    return response.content
