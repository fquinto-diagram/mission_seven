from sqlalchemy import BIGINT, String
from sqlalchemy.orm import relationship
from app.modules.common.models.base_model import BaseModel, SoftDeleteMixin
from sqlalchemy.orm import Mapped, mapped_column
from typing import List, TYPE_CHECKING
from app.modules.roles.tables.role_tables import roles_users, roles_permissions
from app.modules.roles.models.permission_model import Permission

if TYPE_CHECKING:
    from app.modules.users.models.user_model import User

class Role(BaseModel, SoftDeleteMixin):
    __tablename__ = "roles"
    
    DEFAULT_ORDER_BY = "name"
    
    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    
    permissions: Mapped[List["Permission"]] = relationship("Permission", secondary=roles_permissions, back_populates="roles")
    users: Mapped[List["User"]] = relationship("User", secondary=roles_users, back_populates="roles")
    
    def give_permission(self, permission: Permission) -> bool:
        if permission not in [p.name for p in self.permissions]:
            self.permissions.append(permission)
            return True
        return False
    
    
    