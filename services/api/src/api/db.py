from pathlib import Path

from tinydb import TinyDB

DATABASE_PATH = Path(__file__).resolve().parents[2] / "data" / "api.json"


def get_database() -> TinyDB:
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    return TinyDB(DATABASE_PATH)


def get_users_table():
    return get_database().table("users")


def get_profiles_table():
    return get_database().table("profiles")