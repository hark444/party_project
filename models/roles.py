import enum
from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
    Enum,
    DateTime,
    func,
    Table,
    JSON,

)
from sqlalchemy.dialects.postgresql import JSONB, TEXT
from sqlalchemy.orm import relationship, Session
from sqlalchemy.ext.mutable import MutableDict
from datetime import datetime
from models import SessionLocal
from . import Base


class Roles(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    disabled = Column(Boolean, default=False, nullable=False)
