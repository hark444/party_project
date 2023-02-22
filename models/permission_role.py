from sqlalchemy import Column, String, Integer
from models import Base


class PermissionRoleModel(Base):
    __tablename__ = "permission_role"

    id = Column(Integer, primary_key=True, index=True)
    permission_id = Column(Integer, nullable=False)
    role_id = Column(Integer, nullable=False)
