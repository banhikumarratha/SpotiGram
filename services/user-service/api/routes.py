from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from libs.shared.schemas.domain import UserProfile
from libs.shared.schemas.common import ErrorResponse, ErrorDetail
from infrastructure.database.session import get_db
from infrastructure.database.repository import UserRepository
from application.user_service import UserService
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1/users", tags=["Users"])

class CreateUserRequest(BaseModel):
    username: str
    display_name: str | None = None

def get_user_service(db: Session = Depends(get_db)) -> UserService:
    repo = UserRepository(db)
    return UserService(repo)

@router.get("/{user_id}", response_model=UserProfile, responses={404: {"model": ErrorResponse}})
async def get_user(user_id: str, svc: UserService = Depends(get_user_service)):
    profile = svc.get_user_profile(user_id)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=ErrorResponse(success=False, error=ErrorDetail(code="USER_NOT_FOUND", message="User not found")).model_dump()
        )
    return profile

@router.post("", response_model=UserProfile, status_code=status.HTTP_201_CREATED)
async def create_user(req: CreateUserRequest, svc: UserService = Depends(get_user_service)):
    # In reality, catch IntegrityError for duplicate username
    return svc.create_user(req.username, req.display_name)
