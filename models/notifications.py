import enum
from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
    DateTime,
    BigInteger,
    ForeignKey,
    Float,
)
from sqlalchemy.orm import relationship
from datetime import datetime
from models import Base
from models.user import UserModel


class NotificationTypeEnum(str, enum.Enum):
    OPT_IN = "OPT_IN"
    BASIC = "BASIC"


class Notifications(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey("account_user.id"))
    user = relationship(UserModel)
    type = Column(Enum(NotificationTypeEnum), nullable=False, server_default="BASIC")
    is_read = Column(Boolean, nullable=False, default=False)
    expired = Column(Boolean, nullable=False, default=False)
    created_on = Column(DateTime, default=datetime.now(), nullable=False)
    last_modified_on = Column(DateTime, nullable=True)
