from fastapi import APIRouter
from .routes import user

version_router = APIRouter(prefix="/v1")
version_router.include_router(user.user_router)

