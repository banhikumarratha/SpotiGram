from infrastructure.database.repository import UserRepository
from libs.shared.schemas.domain import UserProfile
from typing import Optional

class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def get_user_profile(self, user_id: str) -> Optional[UserProfile]:
        record = self.repo.get_by_id(user_id)
        if not record:
            return None
        return UserProfile(
            id=record.id,
            username=record.username,
            display_name=record.display_name,
            avatar_url=record.avatar_url,
            created_at=record.created_at
        )

    def create_user(self, username: str, display_name: str = None) -> UserProfile:
        record = self.repo.create(username, display_name)
        # Here we would also publish the UserCreatedEvent to the Outbox/Kafka
        return UserProfile(
            id=record.id,
            username=record.username,
            display_name=record.display_name,
            avatar_url=record.avatar_url,
            created_at=record.created_at
        )
