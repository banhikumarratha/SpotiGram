import pytest
import respx
import httpx
from infrastructure.spotify_client import SpotifyClient, SpotifyClientError

@pytest.mark.asyncio
@respx.mock
async def test_get_token():
    respx.post("https://accounts.spotify.com/api/token").respond(200, json={"access_token": "token123"})
    client = SpotifyClient()
    token = await client.get_client_credentials_token()
    assert token == "token123"

@pytest.mark.asyncio
@respx.mock
async def test_search():
    respx.get("https://api.spotify.com/v1/search?q=query&type=track&limit=20").respond(200, json={"tracks": []})
    client = SpotifyClient()
    res = await client.search("token", "query")
    assert "tracks" in res

@pytest.mark.asyncio
@respx.mock
async def test_search_error():
    respx.get("https://api.spotify.com/v1/search?q=query&type=track&limit=20").respond(401)
    client = SpotifyClient()
    with pytest.raises(SpotifyClientError):
        await client.search("token", "query")

@pytest.mark.asyncio
@respx.mock
async def test_get_track():
    respx.get("https://api.spotify.com/v1/tracks/t1").respond(200, json={"id": "t1"})
    client = SpotifyClient()
    res = await client.get_track("token", "t1")
    assert res["id"] == "t1"
