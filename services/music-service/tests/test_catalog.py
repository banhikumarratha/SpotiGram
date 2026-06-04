import pytest
from application.catalog_service import CatalogService
from infrastructure.spotify_client import SpotifyClientError

@pytest.mark.asyncio
async def test_search_success(mocker):
    mocker.patch("application.catalog_service.SpotifyClient.get_client_credentials_token", return_value="token123")
    mocker.patch("application.catalog_service.SpotifyClient.search", return_value={"tracks": []})
    
    service = CatalogService()
    res = await service.search("test")
    assert "tracks" in res

@pytest.mark.asyncio
async def test_get_track_success(mocker):
    mocker.patch("application.catalog_service.SpotifyClient.get_client_credentials_token", return_value="token123")
    mocker.patch("application.catalog_service.SpotifyClient.get_track", return_value={"id": "t1", "name": "Test"})
    
    service = CatalogService()
    res = await service.get_track("t1")
    assert res["id"] == "t1"

@pytest.mark.asyncio
async def test_get_track_error(mocker):
    mocker.patch("application.catalog_service.SpotifyClient.get_client_credentials_token", return_value="token123")
    mocker.patch("application.catalog_service.SpotifyClient.get_track", side_effect=SpotifyClientError("Not Found"))
    
    service = CatalogService()
    with pytest.raises(SpotifyClientError):
        await service.get_track("t1")
