from sqlalchemy import Table, ForeignKey, Column
from app.modules.common.models.base_model import Base
from sqlalchemy import BIGINT

roles_users = Table(
    "roles_users",
    Base.metadata,
    Column("user_id", BIGINT, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("role_id", BIGINT, ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True)
)

roles_permissions = Table(
    "roles_permissions",
    Base.metadata,
    Column("role_id", BIGINT, ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True),
    Column("permission_id", BIGINT, ForeignKey("permissions.id", ondelete="CASCADE"), primary_key=True)
)
