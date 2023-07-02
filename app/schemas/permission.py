from pydantic import BaseModel


class PermissionSchema(BaseModel):
    id: int

    name: str
    description: str

    class Config:
        orm_mode = True


class CreatePermissionSchema(BaseModel):
    name: str
    description: str


class UpdatePermissionSchema(BaseModel):
    name: str | None = None
    description: str | None = None


class ComputedPermissionSchema(PermissionSchema):
    is_in_code: bool = False


# User Permissions
class UserPermissions(BaseModel):
    id: int
    username: str

    permissions: list[PermissionSchema] = []


class CreateUserPermissionSchema(BaseModel):
    user_id: int
    permission_id: int
