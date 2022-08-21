from fastapi import Depends, APIRouter, HTTPException, status
from models.user import UserModel
from models import get_db
from sqlalchemy.orm import Session
from app.api.v1.schema.user import UserSchemaForm
from app.api.v1.schema.response.user import UserResponseSchema
from app.api.v1.routes.auth import get_password_hash

user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.post("/create", response_model=UserResponseSchema)
async def create_user(
    form_data: UserSchemaForm = Depends(), db: Session = Depends(get_db)
):
    try:
        user_obj = UserModel(
            hashed_password=get_password_hash(form_data.password),
            email=form_data.email,
            first_name=form_data.first_name,
            last_name=form_data.first_name,
        )

        db.add(user_obj)
        db.commit()
        db.refresh(user_obj)
        return user_obj

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
