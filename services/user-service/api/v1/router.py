from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from infrastructure.database import get_db
from infrastructure.kafka_publisher import KafkaPublisher
from application.auth_service import AuthService
from application.social_service import SocialService

router = APIRouter(prefix="/api/v1/users", tags=["Users"])
auth_router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])

class RegisterRequest(BaseModel):
    email: str
    password: str
    display_name: str

class LoginRequest(BaseModel):
    email: str
    password: str

publisher = KafkaPublisher(topic="user.events.v1")

@auth_router.post("/register")
async def register(req: RegisterRequest, db: AsyncSession = Depends(get_db)):
    service = AuthService(db, publisher)
    try:
        user = await service.register(req.email, req.password, req.display_name)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@auth_router.post("/login")
async def login(req: LoginRequest, db: AsyncSession = Depends(get_db)):
    service = AuthService(db)
    try:
        token = await service.login(req.email, req.password)
        return token
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

class FollowRequest(BaseModel):
    followed_id: str

@router.post("/{user_id}/follow")
async def follow(user_id: str, req: FollowRequest, db: AsyncSession = Depends(get_db)):
    service = SocialService(db, publisher)
    try:
        res = await service.follow_user(user_id, req.followed_id)
        return res
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
