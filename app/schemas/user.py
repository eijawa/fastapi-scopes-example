from datetime import datetime

from pydantic import BaseModel


class UserSchema(BaseModel):
    id: int

    username: str
    _password: str

    created_at: datetime
    last_access: datetime

    is_active: bool

    is_superuser: bool
    is_staff: bool

    class Config:
        orm_mode = True


class CreateUserSchema(BaseModel):
    username: str
    password: str


class UpdateUserSchema(BaseModel):
    username: str | None = None
    password: str | None = None

    last_access: datetime | None = None

    is_active: bool | None = None

    is_staff: bool | None = None
