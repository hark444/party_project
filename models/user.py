from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
    Enum,
    DateTime,
    DATE,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from datetime import datetime
from models import Base
from models.teams import TeamsModel
from models.role import RoleTypeEnum


class UserModel(Base):
    __tablename__ = "account_user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False, unique=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    disabled = Column(Boolean, default=False, nullable=False)
    hashed_password = Column(String, nullable=True)
    role = Column(Enum(RoleTypeEnum), nullable=False, server_default="regular")
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=True)
    team = relationship(TeamsModel)
    date_of_joining = Column(DATE)
    created_on = Column(DateTime, default=datetime.now(), nullable=False)
    last_modified_on = Column(DateTime, nullable=True)
