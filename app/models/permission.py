from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import ModelBase

from .user import UserModel


class PermissionModel(ModelBase):
    __tablename__ = "permissions"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(32), unique=True)
    description: Mapped[str] = mapped_column(String(256))


class UserPermissionModel(ModelBase):
    __tablename__ = "users_permissions"

    permission_id: Mapped[int] = mapped_column(
        Integer(), ForeignKey("permissions.id"), primary_key=True
    )
    user_id: Mapped[int] = mapped_column(
        Integer(), ForeignKey("users.id"), primary_key=True
    )

    permission: Mapped["PermissionModel"] = relationship(
        "PermissionModel", foreign_keys=[permission_id]
    )
    user: Mapped["UserModel"] = relationship("UserModel", foreign_keys=[user_id])
