from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict

from api.deps import get_current_user
from api.models import Profile, ProfileCreate, User, UserRole
from api.services import create_user_with_profile, delete_user, get_user_by_id, get_user_by_email, get_users, update_user

router = APIRouter(prefix="/users", tags=["users"])


class UserCreate(BaseModel):
    email: str
    password: str
    name: str | None = None
    phone: str | None = None
    address: str | None = None


class UserUpdate(BaseModel):
    email: str | None = None
    password: str | None = None
    role: UserRole | None = None
    is_active: bool | None = None


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    email: str
    is_active: bool
    role: UserRole
    created_at: str


class UserWithProfileResponse(BaseModel):
    user: UserResponse
    profile: Profile


def to_user_response(user: User) -> UserResponse:
    return UserResponse(
        id=user.id,
        email=user.email,
        is_active=user.is_active,
        role=user.role,
        created_at=user.created_at.isoformat(),
    )


def ensure_self_or_admin(current_user: User, target_user_id: str) -> None:
    if current_user.id != target_user_id and current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized for this user.")


@router.post("", response_model=UserWithProfileResponse, status_code=status.HTTP_201_CREATED)
def register_user(payload: UserCreate) -> UserWithProfileResponse:
    if get_user_by_email(payload.email):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User email already exists.")

    user, profile = create_user_with_profile(
        email=payload.email,
        password=payload.password,
        profile=ProfileCreate(name=payload.name, phone=payload.phone, address=payload.address),
    )
    return UserWithProfileResponse(user=to_user_response(user), profile=profile)


@router.get("", response_model=list[UserResponse])
def list_users(current_user: User = Depends(get_current_user)) -> list[UserResponse]:
    return [to_user_response(user) for user in get_users()]


@router.get("/{user_id}", response_model=UserResponse)
def read_user(user_id: str, current_user: User = Depends(get_current_user)) -> UserResponse:
    ensure_self_or_admin(current_user, user_id)
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    return to_user_response(user)


@router.put("/{user_id}", response_model=UserResponse)
def replace_user(user_id: str, payload: UserUpdate, current_user: User = Depends(get_current_user)) -> UserResponse:
    ensure_self_or_admin(current_user, user_id)
    user = update_user(
        user_id=user_id,
        email=payload.email,
        password=payload.password,
        role=payload.role,
        is_active=payload.is_active,
    )
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    return to_user_response(user)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_user(user_id: str, current_user: User = Depends(get_current_user)) -> None:
    ensure_self_or_admin(current_user, user_id)
    if not delete_user(user_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")