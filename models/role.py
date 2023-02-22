from sqlalchemy import Column, String, Integer
from models import Base


class RolesModel(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    role = Column(String, nullable=False, unique=True)
