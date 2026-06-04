import pytest
from application.playback_service import PlaybackService

@pytest.mark.asyncio
async def test_emit_playback_event(mock_publisher):
    service = PlaybackService(publisher=mock_publisher)
    res = await service.emit_playback_event("u1", "t1", "play")
    assert res["status"] == "event_emitted"
    assert res["action"] == "play"
    assert mock_publisher.publish.called
