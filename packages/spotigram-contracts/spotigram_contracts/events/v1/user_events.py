from pydantic import BaseModel
from .base import BaseEvent

class UserCreatedPayload(BaseModel):
    user_id: str
    display_name: str
    email: str

class UserCreatedEvent(BaseEvent):
    payload: UserCreatedPayload

class FriendFollowedPayload(BaseModel):
    follower_id: str
    followed_id: str

class FriendFollowedEvent(BaseEvent):
    payload: FriendFollowedPayload
