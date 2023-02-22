from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from models import Base
from models.permissions import PermissionsModel
from models.role import RolesModel


class PermissionRoleModel(Base):
    __tablename__ = "permission_role"

    id = Column(Integer, primary_key=True, index=True)
    permission_id = Column(Integer, ForeignKey("permissions.id"))
    permission = relationship(PermissionsModel)
    role_id = Column(Integer, ForeignKey("roles.id"))
    role = relationship(RolesModel)
