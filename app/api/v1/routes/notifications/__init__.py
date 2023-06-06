from fastapi import Depends, APIRouter
from app.api.v1.routes.user.auth import oauth2_scheme
from app.api.v1.routes.notifications.notifications import notifications_router

PROTECTED = [Depends(oauth2_scheme)]

notifications_base_router = APIRouter(prefix="", dependencies=PROTECTED)
notifications_base_router.include_router(notifications_router)
