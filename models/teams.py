from sqlalchemy import Column, String, DateTime, Integer
from datetime import datetime
from models import Base


class TeamsModel(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    team_name = Column(String, nullable=False)
    created_on = Column(DateTime, default=datetime.now(), nullable=False)
    last_modified_on = Column(DateTime, nullable=True)
