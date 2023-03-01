from fastapi import Depends, APIRouter
from app.api.v1.routes.user.auth import oauth2_scheme
from app.api.v1.routes.opt_in.opt_in_handler import opt_in_router

PROTECTED = [Depends(oauth2_scheme)]

opt_in_base_router = APIRouter(prefix="", dependencies=PROTECTED)
opt_in_base_router.include_router(opt_in_router)
