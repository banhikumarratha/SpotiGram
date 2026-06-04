from sqlalchemy.orm import Session
from infrastructure.database.models import UserRecord
from typing import Optional

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: str) -> Optional[UserRecord]:
        return self.db.query(UserRecord).filter(UserRecord.id == user_id).first()

    def get_by_username(self, username: str) -> Optional[UserRecord]:
        return self.db.query(UserRecord).filter(UserRecord.username == username).first()

    def create(self, username: str, display_name: str = None) -> UserRecord:
        user = UserRecord(username=username, display_name=display_name)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
