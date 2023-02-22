from sqlalchemy import Column, String, DateTime, Integer
from datetime import datetime
from models import Base


class PermissionsModel(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)
    permission = Column(String, nullable=False, unique=True)
