from fastapi import Depends, APIRouter, HTTPException, status
from app.api.v1.routes.auth import oauth2_scheme
from .party import party_party_router

PROTECTED = [Depends(oauth2_scheme)]

party_router = APIRouter(prefix="/user/{user_id}", dependencies=PROTECTED)
party_router.include_router(party_party_router)
