from datetime import UTC, datetime
from uuid import uuid4

from tinydb import Query

from api.db import get_notes_table, get_profiles_table, get_records_table, get_users_table
from api.models import Profile, ProfileCreate, Record, RecordNote, RecordStage, RecordStatus, User, UserRole, create_profile, create_user
from api.security import hash_password
from uuid import uuid4

# ---------------------------------------------------------------------------
# User services
# ---------------------------------------------------------------------------


def create_user_with_profile(
    email: str,
    password: str,
    role: UserRole = UserRole.USER,
    is_active: bool = True,
    profile: ProfileCreate | None = None,
) -> tuple[User, Profile]:
    user = create_user(email=email, password=password, role=role, is_active=is_active)
    linked_profile = create_profile(user.id, profile or ProfileCreate())
    return user, linked_profile


def get_users() -> list[User]:
    return [User.model_validate(user) for user in get_users_table().all()]


def get_user_by_id(user_id: str) -> User | None:
    UserQuery = Query()
    user = get_users_table().get(UserQuery.id == user_id)
    return User.model_validate(user) if user else None


def get_user_by_email(email: str) -> User | None:
    UserQuery = Query()
    user = get_users_table().get(UserQuery.email == email)
    return User.model_validate(user) if user else None


def update_user(
    user_id: str,
    email: str | None = None,
    password: str | None = None,
    role: UserRole | None = None,
    is_active: bool | None = None,
) -> User | None:
    update_data: dict[str, object] = {}
    if email is not None:
        update_data["email"] = email
    if password is not None:
        update_data["hashed_password"] = hash_password(password)
    if role is not None:
        update_data["role"] = role.value
    if is_active is not None:
        update_data["is_active"] = is_active

    if update_data:
        UserQuery = Query()
        get_users_table().update(update_data, UserQuery.id == user_id)

    return get_user_by_id(user_id)


def delete_user(user_id: str) -> bool:
    UserQuery = Query()
    ProfileQuery = Query()
    removed_users = get_users_table().remove(UserQuery.id == user_id)
    get_profiles_table().remove(ProfileQuery.user_id == user_id)
    return len(removed_users) > 0


def get_profile_by_user_id(user_id: str) -> Profile | None:
    ProfileQuery = Query()
    profile = get_profiles_table().get(ProfileQuery.user_id == user_id)
    return Profile.model_validate(profile) if profile else None


def update_profile(user_id: str, name: str | None = None, phone: str | None = None, address: str | None = None) -> Profile | None:
    update_data = {key: value for key, value in {"name": name, "phone": phone, "address": address}.items() if value is not None}

    if update_data:
        ProfileQuery = Query()
        get_profiles_table().update(update_data, ProfileQuery.user_id == user_id)

    return get_profile_by_user_id(user_id)

# ---------------------------------------------------------------------------
# Record services
# ---------------------------------------------------------------------------


def create_record(
    full_name: str,
    email: str,
    phone: str,
    position: str,
    linkedin_url: str | None = None,
    cv_url: str | None = None,
    status: RecordStatus = RecordStatus.RECEIVED,
    stage: RecordStage = RecordStage.PENDING,
    experience_years: int = 0,
) -> Record:
    now = datetime.now(UTC)
    record = Record(
        id=str(uuid4()),
        full_name=full_name,
        email=email,
        phone=phone,
        position=position,
        linkedin_url=linkedin_url,
        cv_url=cv_url,
        status=status,
        stage=stage,
        experience_years=experience_years,
        applied_at=now,
        updated_at=now,
    )
    get_records_table().insert(record.model_dump(mode="json"))
    return record


def get_records() -> list[Record]:
    records: list[Record] = []
    for raw in get_records_table().all():
        record = Record.model_validate(raw)
        record.notes = [RecordNote.model_validate(n) for n in get_notes_table().search(Query().record_id == record.id)]
        record.notes_count = len(record.notes)
        records.append(record)
    return records


def get_record_by_id(record_id: str) -> Record | None:
    raw = get_records_table().get(Query().id == record_id)
    if not raw:
        return None
    record = Record.model_validate(raw)
    record.notes = [RecordNote.model_validate(n) for n in get_notes_table().search(Query().record_id == record.id)]
    record.notes_count = len(record.notes)
    return record


def update_record(
    record_id: str,
    full_name: str | None = None,
    email: str | None = None,
    phone: str | None = None,
    position: str | None = None,
    linkedin_url: str | None = None,
    cv_url: str | None = None,
    status: RecordStatus | None = None,
    stage: RecordStage | None = None,
    experience_years: int | None = None,
) -> Record | None:
    update_data: dict[str, object] = {}
    if full_name is not None:
        update_data["full_name"] = full_name
    if email is not None:
        update_data["email"] = email
    if phone is not None:
        update_data["phone"] = phone
    if position is not None:
        update_data["position"] = position
    if linkedin_url is not None:
        update_data["linkedin_url"] = linkedin_url
    if cv_url is not None:
        update_data["cv_url"] = cv_url
    if status is not None:
        update_data["status"] = status.value
    if stage is not None:
        update_data["stage"] = stage.value
    if experience_years is not None:
        update_data["experience_years"] = experience_years

    if update_data:
        update_data["updated_at"] = datetime.now(UTC)
        get_records_table().update(update_data, Query().id == record_id)

    return get_record_by_id(record_id)


def patch_record_status(record_id: str, status: RecordStatus | None = None, stage: RecordStage | None = None) -> Record | None:
    update_data: dict[str, object] = {}
    if status is not None:
        update_data["status"] = status.value
    if stage is not None:
        update_data["stage"] = stage.value

    if update_data:
        update_data["updated_at"] = datetime.now(UTC)
        get_records_table().update(update_data, Query().id == record_id)

    return get_record_by_id(record_id)


def delete_record(record_id: str) -> bool:
    removed = get_records_table().remove(Query().id == record_id)
    get_notes_table().remove(Query().record_id == record_id)
    return len(removed) > 0


# ---------------------------------------------------------------------------
# Note services
# ---------------------------------------------------------------------------


def add_note(record_id: str, content: str) -> RecordNote:
    note = RecordNote(id=str(uuid4()), record_id=record_id, content=content, created_at=datetime.now(UTC))
    get_notes_table().insert(note.model_dump(mode="json"))
    return note


def delete_note(record_id: str, note_id: str) -> bool:
    removed = get_notes_table().remove((Query().id == note_id) & (Query().record_id == record_id))
    return len(removed) > 0