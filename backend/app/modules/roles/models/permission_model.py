from sqlalchemy import BIGINT, String
from sqlalchemy.orm import relationship
from app.modules.common.models.base_model import BaseModel, SoftDeleteMixin
from sqlalchemy.orm import Mapped, mapped_column
from typing import List, TYPE_CHECKING
from app.modules.roles.tables.role_tables import roles_permissions

if TYPE_CHECKING:
    from app.modules.roles.models.role_model import Role

class Permission(BaseModel, SoftDeleteMixin):
    __tablename__ = "permissions"
    
    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    
    roles: Mapped[List["Role"]] = relationship("Role", secondary=roles_permissions, back_populates="permissions")
    
    