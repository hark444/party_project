from sqlalchemy import Column, String, Integer
from models import Base
import enum


PERMISSIONS = {
    "CREATE_ADMIN": "create_admin",
    "ADD_USER_TO_TEAM": "add_user_to_team",
    "REMOVE_USER_FROM_TEAM": "remove_user_from_team",
    "SEND_EMAIL": "send_email",
    "CREATE_PARTY": "create_party",
}


class PermissionsModel(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)
    permission = Column(String, nullable=False, unique=True)
