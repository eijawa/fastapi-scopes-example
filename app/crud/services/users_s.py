from datetime import datetime

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.core.security import password_manager
from app.models import UserModel
from app.schemas.user import CreateUserSchema, UpdateUserSchema
from app.core.security.permissions import PermissionsGroups

from .service import BaseService
from .permissions_s import UsersPermissionsService


class UsersService(BaseService[UserModel, CreateUserSchema, UpdateUserSchema]):
    model = UserModel

    @classmethod
    def create(cls, session: Session, *, obj: CreateUserSchema) -> UserModel:
        """
        Создание пользователя с базовым набором прав
        """

        data = jsonable_encoder(obj)
        data["password"] = password_manager.hash(data["password"])

        o = cls.model(**data)

        session.add(o)
        session.commit()
        session.refresh(o)

        # Связать пользователя с правами
        UsersPermissionsService.link(
            session,
            user=o,
            permissions_groups=[PermissionsGroups.default],
        )

        return o

    @classmethod
    def create_superuser(cls, session: Session, *, obj: CreateUserSchema) -> UserModel:
        """
        Создание пользователя с полным набором прав
        """

        o = cls.create(session, obj=obj)

        o.is_superuser = True

        session.add(o)
        session.commit()
        session.refresh(o)

        # Связать пользователя с правами
        UsersPermissionsService.link(
            session,
            user=o,
            permissions=[
                *(PermissionsGroups.admin.value - PermissionsGroups.default.value)
            ],
        )

        return o

    @classmethod
    def activate(cls, session: Session, *, obj: UserModel) -> None:
        upd_data = UpdateUserSchema(is_active=True)

        cls.update(session, obj=obj, upd_obj=upd_data)

    @classmethod
    def deactivate(cls, session: Session, *, obj: UserModel) -> None:
        upd_data = UpdateUserSchema(is_active=False)

        cls.update(session, obj=obj, upd_obj=upd_data)

    @classmethod
    def rehash_password(
        cls, session: Session, *, obj: UserModel, password: str
    ) -> None:
        upd_data = UpdateUserSchema(password=password_manager.hash(password))

        cls.update(session, obj=obj, upd_obj=upd_data)

    @classmethod
    def update_last_access(cls, session: Session, *, obj: UserModel) -> None:
        upd_data = UpdateUserSchema(last_access=datetime.now())

        cls.update(session, obj=obj, upd_obj=upd_data)
