from app.api.v1.routes.auth import get_current_user
from fastapi import Depends, HTTPException
from models.user import UserModel
from typing import List
import logging

logger = logging.getLogger("main")


class ValidatePermissions:
    def __init__(self, allowed_roles: List):
        self.allowed_roles = allowed_roles

    def __call__(self, user: UserModel = Depends(get_current_user)):
        if user.role not in self.allowed_roles:
            logger.warning(f"User with role {user.role} not in {self.allowed_roles}")
            raise HTTPException(status_code=403, detail="Not enough permissions.")
