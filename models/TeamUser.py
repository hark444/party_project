from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from models import Base
from models.user import UserModel


class TeamUserModel(Base):
    __tablename__ = "team_user"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String, unique=True)
    user_id = Column(Integer, ForeignKey("account_user.id"))
    user = relationship(UserModel)
    subscribed = Column(Boolean, default=False)
    deleted = Column(Boolean, default=False)
    created_on = Column(DateTime, default=datetime.now(), nullable=False)
    last_modified_on = Column(DateTime, nullable=True)
