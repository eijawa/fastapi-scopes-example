from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import UserModel

from .repository import BaseRepository


class UsersRepository(BaseRepository[UserModel]):
    model = UserModel

    @classmethod
    def get_by_username(cls, session: Session, *, username: str) -> UserModel | None:
        stmt = select(cls.model).where(cls.model.username == username)
        return session.scalars(stmt).first()
