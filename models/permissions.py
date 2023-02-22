from sqlalchemy import Column, String, Integer
from models import Base


class PermissionsModel(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)
    permission = Column(String, nullable=False, unique=True)
