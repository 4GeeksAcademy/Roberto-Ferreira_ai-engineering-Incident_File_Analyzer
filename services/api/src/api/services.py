from tinydb import Query

from api.db import get_profiles_table, get_users_table
from api.models import Profile, ProfileCreate, User, UserRole, create_profile, create_user
from api.security import hash_password


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