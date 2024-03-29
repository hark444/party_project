from fastapi import Depends, FastAPI, APIRouter, HTTPException, status, Request
from models.user import UserModel, RoleTypeEnum
from models import get_db
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from pydantic import BaseModel
from app.api.v1.schema.response.user import UserResponseSchema
from app.api.v1.schema.request.role import RoleTypeSchema
from utils.authorization import ValidatePermissions

user_role_router = APIRouter(prefix="/user-role", tags=["roles"])

allow_change_role = ValidatePermissions(["superuser"])
"""
Role change is currently limited to superusers only. A superuser can change any users role
to either superuser, admin or regular user.
"""


@user_role_router.patch(
    "/{user_id}",
    response_model=UserResponseSchema,
    dependencies=[Depends(allow_change_role)],
)
async def login_for_access_token(
    user_id: int,
    role: RoleTypeSchema,
    db: Session = Depends(get_db),
):
    try:
        user = db.query(UserModel).filter_by(id=user_id).one_or_none()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found with this ID",
            )
        user.role = role.role

        db.add(user)
        db.commit()
        db.refresh(user)

        return user
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
