from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from infrastructure.models import UserAccount, UserProfile
from passlib.hash import bcrypt
import jwt
import os
from datetime import datetime, timedelta
import uuid

JWT_SECRET = os.getenv("JWT_SECRET", "spotigram-dev-secret")
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

class AuthService:
    def __init__(self, session: AsyncSession, publisher=None):
        self.session = session
        self.publisher = publisher

    async def register(self, email: str, password: str, display_name: str) -> dict:
        result = await self.session.execute(select(UserAccount).where(UserAccount.email == email))
        if result.scalar_one_or_none():
            raise ValueError("Email already exists")

        hashed_password = bcrypt.hash(password)
        new_user = UserAccount(email=email, password_hash=hashed_password)
        self.session.add(new_user)
        await self.session.flush()

        profile = UserProfile(user_id=new_user.id, display_name=display_name)
        self.session.add(profile)
        await self.session.commit()

        if self.publisher:
            event = {
                "headers": {
                    "event_id": str(uuid.uuid4()),
                    "correlation_id": "none",
                    "idempotency_key": str(uuid.uuid4()),
                    "timestamp": datetime.utcnow().isoformat(),
                    "version": "v1"
                },
                "payload": {
                    "user_id": new_user.id,
                    "display_name": display_name,
                    "email": email
                }
            }
            await self.publisher.publish(event)

        return {"user_id": new_user.id, "email": email}

    async def login(self, email: str, password: str) -> dict:
        result = await self.session.execute(select(UserAccount).where(UserAccount.email == email))
        user = result.scalar_one_or_none()
        
        if not user or not bcrypt.verify(password, user.password_hash):
            raise ValueError("Invalid credentials")

        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        payload = {"sub": user.id, "exp": expire}
        token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
        
        return {"access_token": token, "token_type": "bearer"}
