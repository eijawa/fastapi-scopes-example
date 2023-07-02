from app.core.security.permissions import Permissions


def required_permissions_str(*permissions: Permissions) -> str:
    return f"Требуемые права: {','.join([f'`{p.value.key}`' for p in permissions])}"
