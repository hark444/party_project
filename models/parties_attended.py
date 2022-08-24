import enum
from sqlalchemy import Boolean, Column, Integer, Text, DateTime, BigInteger, ForeignKey, Float
from sqlalchemy.dialects.postgresql import JSONB, TEXT
from sqlalchemy.orm import relationship
from datetime import datetime
from models import Base
from models.party import Party
from models.user import UserModel


class PartiesAttended(Base):
    __tablename__ = "parties_attended"

    id = Column(Integer, primary_key=True, index=True)
    party_id = Column(BigInteger, ForeignKey('party.id'))
    party = relationship(Party)
    user_id = Column(BigInteger, ForeignKey('account_user.id'))
    user = relationship(UserModel)
    rating = Column(Float, nullable=True)
    approved = Column(Boolean, nullable=False, default=False)
    comment = Column(Text, nullable=True)
