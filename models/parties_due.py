import enum
from sqlalchemy import Column, Integer, BigInteger, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from models import Base
from models.user import UserModel


class PartiesDue(Base):
    __tablename__ = "parties_due"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey('account_user.id'))
    user = relationship(UserModel)
    parties_due = Column(Integer, nullable=False, default=0)
