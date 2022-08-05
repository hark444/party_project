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
from models import Base


class UserModel(Base):
    __tablename__ = "account_user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False, unique=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    disabled = Column(Boolean, default=False, nullable=False)
    hashed_password = Column(String, nullable=True)
    created_on = Column(DateTime, default=datetime.now(), nullable=False)
    last_modified_on = Column(DateTime, nullable=True)

