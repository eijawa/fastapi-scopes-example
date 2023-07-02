from datetime import datetime, timedelta
from typing import Any

from argon2 import PasswordHasher
from jose import JWTError, jwt
from pydantic import BaseModel

from app.core import common
from app.core.settings import settings


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: int | None = None
    username: str | None = None

    scopes: list[str] = []


def create_access_token(data: TokenData, expires_delta: timedelta | None = None) -> str:
    data_: dict[str, Any] = data.dict()

    if expires_delta is None:
        expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    expire = datetime.utcnow() + expires_delta
    data_["exp"] = expire

    token: str = jwt.encode(
        data_, settings.PROJECT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )

    return token


def decode_token(token: str) -> TokenData | None:
    try:
        payload = jwt.decode(
            token, settings.PROJECT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )

        del payload["exp"]

        return TokenData(**payload)  # type: ignore
    except JWTError:
        return None


class PasswordManager(metaclass=common.Singleton):
    """
    Обёртка поверх модуля argon2.
    На случай, если потребуется изменение методов хэширования
    """

    def __new__(cls, *args, **kwargs):
        cls.ph = PasswordHasher()

        return super().__new__(cls, *args, **kwargs)

    @classmethod
    def hash(cls, password: str) -> str:
        return cls.ph.hash(password)

    @classmethod
    def verify(cls, hash: str, password: str) -> bool:
        try:
            return cls.ph.verify(hash, password)
        except Exception:
            return False

    @classmethod
    def check_needs_rehash(cls, hash: str) -> bool:
        return cls.ph.check_needs_rehash(hash)


password_manager = PasswordManager()
