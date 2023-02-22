from sqlalchemy import Column, String, Integer
from models import Base
import enum


class RoleTypeEnum(str, enum.Enum):
    admin = "admin"
    superuser = "superuser"
    regular = "regular"


class RolesModel(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    role = Column(String, nullable=False, unique=True)
