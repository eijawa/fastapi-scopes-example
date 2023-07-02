from typing import Sequence, Iterable

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security.permissions import Permissions
from app.models import PermissionModel, UserModel, UserPermissionModel

from .repository import BaseRepository


class PermissionsRepository(BaseRepository[PermissionModel]):
    model = PermissionModel

    @classmethod
    def get_by_name(cls, session: Session, *, name: str) -> PermissionModel | None:
        """
        Единичное получение по ключу\имени -> item:verb
        """

        stmt = select(cls.model).where(cls.model.name == name)
        
        return session.scalars(stmt).first()

    @classmethod
    def get_all_by_names(
        cls, session: Session, *, names: Iterable[str]
    ) -> Sequence[PermissionModel]:
        """
        Множественное получение по списку ключей\имён
        """

        stmt = select(cls.model).where(cls.model.name.in_(names))

        return session.scalars(stmt).all()

    @classmethod
    def check_db_sync(cls, session: Session) -> bool:
        """
        Проверка соответствия Permissions в коде и в базе.
        В коде могут быть не все Permissions из базы, но не наоборот
        """

        perms_in_db: list[PermissionModel] = cls.all(session)
        perms_in_db_keys: list[str] = [p.name for p in perms_in_db]

        for perm in Permissions.__members__.values():
            if str(perm) not in perms_in_db_keys:
                return False

        return True


class UsersPermissionsRepository(BaseRepository[UserPermissionModel]):
    model = UserPermissionModel

    @classmethod
    def get_by_user(
        cls, session: Session, *, user: UserModel
    ) -> Sequence[UserPermissionModel]:
        stmt = (
            select(cls.model)
            .join(UserModel)
            .join(PermissionModel)
            .where(cls.model.user_id == user.id)
        )

        return session.scalars(stmt).all()

    @classmethod
    def has(cls, session: Session, *, user: UserModel, permissions: list[str]) -> bool:
        """
        Метод проверки, что пользователь на самом деле обладает запрашиваемым набором прав
        """

        stmt = (
            select(cls.model)
            .join(UserModel)
            .join(PermissionModel)
            .where(
                cls.model.user_id == user.id,
                PermissionModel.name.in_(permissions),
            )
        )

        res = session.scalars(stmt).all()

        # Логика простая:
        # Если пользователь запросил 5 прав,
        # но из этих 5 прав у него есть доступ только к 4,
        # то мы возвращаем False.
        # Если запросил 5 прав и вернулось 5 прав
        # (обрати внимание, что в базе у него может быть и 10 прав,
        # но мы сверяем только по тем, что он запросил),
        # то мы возвращаем True, тк он обладает всеми правами, что запросил.
        return len(res) == len(permissions)
