from dataclasses import dataclass
from enum import Enum, unique


@dataclass
class PermissionsData:
    key: str
    description: str


@unique
class Permissions(Enum):
    users_me = PermissionsData(
        "users:me", "Чтение, изменение и удаление данных пользователя о себе"
    )

    users_read = PermissionsData(
        "users:read", "Чтение данных обо всех пользователях в системе"
    )
    users_create = PermissionsData("users:create", "Создание новых пользователей")
    users_update = PermissionsData("users:update", "Изменение данных пользователей")
    users_delete = PermissionsData("users:delete", "Удаление пользователей")

    permissions_me = PermissionsData(
        "permissions:me", "Чтение пользователем набора своих прав"
    )
    permissions_read = PermissionsData(
        "permissions:read", "Чтение данных обо всех правах в системе"
    )
    permissions_create = PermissionsData(
        "permissions:create", "Присвоение новых прав пользователям"
    )
    permissions_delete = PermissionsData(
        "permissions:delete", "Удаление прав у пользователей"
    )

    @classmethod
    def dict(cls) -> dict[str, str]:
        return {p.value.key: p.value.description for p in cls.__members__.values()}  # type: ignore

    def __str__(self) -> str:
        return self.value.key


@unique
class PermissionsGroups(Enum):
    """
    Группы прав.

    Каждая группа должна иметь уникальные (специфичные) для группы права.
    """

    default = set([Permissions.users_me, Permissions.permissions_me])

    admin = set(Permissions.__members__.values())

    staff = set([Permissions.users_read])
