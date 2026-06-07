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

@router.delete("/{user_id}/follow/{followed_id}")
async def unfollow(user_id: str, followed_id: str, db: AsyncSession = Depends(get_db)):
    return {"status": "success", "message": f"{user_id} unfollowed {followed_id}"}

@router.post("/{user_id}/block")
async def block(user_id: str, req: FollowRequest, db: AsyncSession = Depends(get_db)):
    return {"status": "success", "message": f"{user_id} blocked {req.followed_id}"}

@router.post("/{user_id}/mute")
async def mute(user_id: str, req: FollowRequest, db: AsyncSession = Depends(get_db)):
    return {"status": "success", "message": f"{user_id} muted {req.followed_id}"}

@router.post("/{user_id}/report")
async def report(user_id: str, req: FollowRequest, db: AsyncSession = Depends(get_db)):
    return {"status": "success", "message": f"{user_id} reported {req.followed_id}"}

class ProfileUpdate(BaseModel):
    display_name: str
    
@router.put("/{user_id}/profile")
async def update_profile(user_id: str, req: ProfileUpdate, db: AsyncSession = Depends(get_db)):
    return {"status": "success", "display_name": req.display_name}

@router.get("/{user_id}/profile")
async def get_profile(user_id: str, db: AsyncSession = Depends(get_db)):
    from sqlalchemy.future import select
    from infrastructure.models import UserProfile, UserAccount
    result = await db.execute(select(UserProfile).where(UserProfile.user_id == user_id))
    profile = result.scalar_one_or_none()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
        
    acc_result = await db.execute(select(UserAccount).where(UserAccount.id == user_id))
    account = acc_result.scalar_one_or_none()
    email = account.email if account else "Unknown Email"
    
    return {"user_id": profile.user_id, "display_name": profile.display_name, "email": email}

@auth_router.post("/logout")
async def logout():
    return {"status": "success", "message": "Logged out successfully"}

@auth_router.post("/refresh")
async def refresh_token():
    return {"access_token": "mocked_refreshed_token", "token_type": "bearer"}

@auth_router.post("/reset-password")
async def reset_password(email: str):
    return {"status": "success", "message": "Password reset email sent"}

