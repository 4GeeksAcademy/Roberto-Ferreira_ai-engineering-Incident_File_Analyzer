from functools import lru_cache
from os import getenv

from dotenv import load_dotenv

load_dotenv()


class Settings:
    def __init__(self) -> None:
        self.secret_key = self._required("SECRET_KEY")
        self.jwt_algorithm = self._required("JWT_ALGORITHM")
        self.access_token_expire_minutes = int(getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

    @staticmethod
    def _required(name: str) -> str:
        value = getenv(name)
        if not value:
            raise RuntimeError(f"{name} is not configured.")
        return value


@lru_cache
def get_settings() -> Settings:
    return Settings()