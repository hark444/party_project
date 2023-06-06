import enum


class RoleTypeEnum(str, enum.Enum):
    admin = "admin"
    superuser = "superuser"
    regular = "regular"
