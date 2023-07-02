from abc import ABC
from typing import Any, Generic, Type

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.core.typings import CreateSchemaType, ModelType, UpdateSchemaType


class BaseService(Generic[ModelType, CreateSchemaType, UpdateSchemaType], ABC):
    """
    Сервис для работы с данными: создание, обновление, удаление.
    Подсмотренно здесь:
    https://github.com/tiangolo/full-stack-fastapi-postgresql/blob/master/%7B%7Bcookiecutter.project_slug%7D%7D/backend/app/app/crud/base.py
    """

    model: Type[ModelType]

    @classmethod
    def create(cls, session: Session, *, obj: CreateSchemaType) -> ModelType:
        data = jsonable_encoder(obj)

        o = cls.model(**data)

        session.add(o)
        session.commit()
        session.refresh(o)

        return o

    @classmethod
    def update(
        cls,
        session: Session,
        *,
        obj: ModelType,
        upd_obj: UpdateSchemaType | dict[str, Any]
    ) -> ModelType:
        data = jsonable_encoder(obj)
        
        if isinstance(upd_obj, dict):
            update_data = upd_obj
        else:
            update_data = upd_obj.dict(exclude_unset=True)

        for field in data:
            if field in update_data:
                setattr(obj, field, update_data[field])
        
        session.add(obj)
        session.commit()
        session.refresh(obj)

        return obj

    @classmethod
    def delete(cls, session: Session, *, pk: Any) -> bool:
        try:
            obj = session.query(cls.model).get(pk)

            session.delete(obj)
            session.commit()

            return True
        except Exception:
            return False
