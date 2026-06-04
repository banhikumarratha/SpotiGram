from libs.shared.schemas.common import ErrorResponse, ErrorDetail
from libs.shared.schemas.events import BaseEventEnvelope
import pytest

def test_error_response_creation():
    detail = ErrorDetail(code="NOT_FOUND", message="Resource not found")
    resp = ErrorResponse(success=False, error=detail)
    assert not resp.success
    assert resp.error.code == "NOT_FOUND"

def test_base_event_envelope_defaults():
    env = BaseEventEnvelope(
        correlation_id="123",
        event_type="TestEvent",
        payload={"key": "value"}
    )
    assert env.event_id is not None
    assert env.version == "1.0"
    assert env.timestamp is not None
