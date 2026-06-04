"""
PlaylistService — generates themed playlists via the tool chain.
"""
from typing import Optional

from domain.models import UserContext, GeneratedPlaylist
from domain.ports import AIProviderPort
from chains.tool_chain import generate_playlist, explain_recommendation


class PlaylistService:
    def __init__(self, provider: AIProviderPort):
        self._provider = provider

    async def create(
        self,
        theme: str,
        context: Optional[UserContext] = None,
        mood: str = "any",
        prompt_version: str = "v1",
    ) -> GeneratedPlaylist:
        return await generate_playlist(
            theme=theme,
            provider=self._provider,
            context=context,
            mood=mood,
            prompt_version=prompt_version,
        )

    async def explain(
        self,
        track_title: str,
        track_artist: str,
        signals: dict,
        context: Optional[UserContext] = None,
        prompt_version: str = "v1",
    ) -> str:
        return await explain_recommendation(
            track_title=track_title,
            track_artist=track_artist,
            signals=signals,
            provider=self._provider,
            context=context,
            prompt_version=prompt_version,
        )
