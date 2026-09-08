from datetime import UTC, datetime
from enum import StrEnum
from uuid import uuid4

from pydantic import BaseModel, ConfigDict

from api.db import get_profiles_table, get_users_table
from api.security import hash_password


class UserRole(StrEnum):
    ADMIN = "admin"
    MANAGER = "manager"
    USER = "user"


class User(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    id: str
    email: str
    hashed_password: str
    is_active: bool
    role: UserRole = UserRole.USER
    created_at: datetime


class Profile(BaseModel):
    id: str
    user_id: str
    name: str | None = None
    phone: str | None = None
    address: str | None = None


class ProfileCreate(BaseModel):
    name: str | None = None
    phone: str | None = None
    address: str | None = None


def create_user(email: str, password: str, role: UserRole = UserRole.USER, is_active: bool = True) -> User:
    user = User(
        id=str(uuid4()),
        email=email,
        hashed_password=hash_password(password),
        is_active=is_active,
        role=role,
        created_at=datetime.now(UTC),
    )
    get_users_table().insert(user.model_dump(mode="json"))
    return user


def create_profile(user_id: str, profile: ProfileCreate) -> Profile:
    created_profile = Profile(id=str(uuid4()), user_id=user_id, **profile.model_dump())
    get_profiles_table().insert(created_profile.model_dump(mode="json"))
    return created_profile