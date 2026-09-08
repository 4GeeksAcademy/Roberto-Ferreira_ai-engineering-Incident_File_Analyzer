from fastapi import APIRouter, HTTPException, status
from fastapi import Depends
from pydantic import BaseModel

from api.deps import get_current_user
from api.models import Profile, User, UserRole
from api.security import create_access_token, verify_password
from api.services import get_profile_by_user_id, get_user_by_email

router = APIRouter(prefix="/auth", tags=["auth"])


class LoginRequest(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class CurrentUserResponse(BaseModel):
    email: str
    role: UserRole
    profile: Profile | None


@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest) -> LoginResponse:
    user = get_user_by_email(payload.email)
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password.")

    return LoginResponse(access_token=create_access_token(subject=user.id))


@router.get("/me", response_model=CurrentUserResponse)
def read_current_user(current_user: User = Depends(get_current_user)) -> CurrentUserResponse:
    return CurrentUserResponse(
        email=current_user.email,
        role=current_user.role,
        profile=get_profile_by_user_id(current_user.id),
    )