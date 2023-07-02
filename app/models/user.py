from datetime import datetime

from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, validates

from app.core.db import ModelBase


class UserModel(ModelBase):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    username: Mapped[str] = mapped_column(String(16), unique=True)
    password: Mapped[str] = mapped_column(String(32))

    created_at: Mapped[datetime] = mapped_column(
        DateTime(), insert_default=datetime.now
    )
    last_access: Mapped[datetime] = mapped_column(
        DateTime(), insert_default=datetime.now
    )

    is_active: Mapped[bool] = mapped_column(Boolean(), default=True)

    is_superuser: Mapped[bool] = mapped_column(Boolean(), default=False)
    is_staff: Mapped[bool] = mapped_column(Boolean(), default=False)

    @validates("created_at")
    def validate_created_at(self, key, value):
        if self.created_at:
            raise ValueError("created_at is read-only")

        return value
