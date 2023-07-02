from abc import ABC
from typing import Generic, Any, Type
from sqlalchemy.orm import Session

from app.core.typings import ModelType


class BaseRepository(Generic[ModelType], ABC):
    """
    Репозиторий для получения данных из БД.
    Подсмотрено здесь:
    https://github.com/tiangolo/full-stack-fastapi-postgresql/blob/master/%7B%7Bcookiecutter.project_slug%7D%7D/backend/app/app/crud/base.py
    """

    model: Type[ModelType]

    @classmethod
    def all(cls, session: Session) -> list[ModelType]:
        return session.query(cls.model).all()

    @classmethod
    def get(cls, session: Session, *, pk: Any) -> ModelType | None:
        return session.query(cls.model).get(pk)

    @classmethod
    def exists(cls, session: Session, *, pk: Any) -> bool:
        return cls.get(session, pk=pk) is not None
