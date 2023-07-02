from fastapi import APIRouter

from .endpoints import auth, users, permissions


router = APIRouter()
router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(users.router, prefix="/users", tags=["users"])
router.include_router(permissions.router, tags=["permissions"])
