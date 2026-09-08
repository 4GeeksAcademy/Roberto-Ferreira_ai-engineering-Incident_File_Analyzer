from datetime import UTC, datetime
from enum import StrEnum
from uuid import uuid4

from pydantic import BaseModel, ConfigDict

from api.db import get_profiles_table, get_records_table as _get_records_table, get_users_table
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


class RecordStatus(StrEnum):
    RECEIVED = "received"
    IN_PROGRESS = "in_progress"
    SELECTED = "selected"
    DISCARDED = "discarded"


class RecordStage(StrEnum):
    PENDING = "pending"
    REVIEW = "review"
    PERSONAL_INTERVIEW = "personal_interview"
    TECHNICAL_INTERVIEW = "technical_interview"
    OFFER_PRESENTED = "offer_presented"


class RecordNote(BaseModel):
    id: str
    record_id: str
    content: str
    created_at: datetime


class Record(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    id: str
    full_name: str
    email: str
    phone: str
    position: str
    linkedin_url: str | None = None
    cv_url: str | None = None
    status: RecordStatus = RecordStatus.RECEIVED
    stage: RecordStage = RecordStage.PENDING
    experience_years: int = 0
    applied_at: datetime
    updated_at: datetime
    notes_count: int = 0
    notes: list[RecordNote] = []


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