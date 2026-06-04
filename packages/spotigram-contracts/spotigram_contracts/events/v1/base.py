from pydantic import BaseModel
from ...common import EventHeaders

class BaseEvent(BaseModel):
    headers: EventHeaders
