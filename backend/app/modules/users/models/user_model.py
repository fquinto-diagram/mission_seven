from sqlalchemy import String, BIGINT
from sqlalchemy.orm import Mapped, mapped_column, deferred
from app.modules.common.models.base_model import BaseModel, SoftDeleteMixin
from typing import List
from sqlalchemy.orm import relationship
from datetime import datetime
from app.adapters.bcrypt_adapter import BcryptAdapter
from app.modules.roles.tables.role_tables import roles_users
from app.modules.roles.models.role_model import Role
from app.modules.auth.models.reset_password_token_model import ResetPasswordToken

    
class User(BaseModel, SoftDeleteMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    surname: Mapped[str] = mapped_column(String(100), nullable=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    password: Mapped[str] = deferred(mapped_column(String(255), nullable=False))
    lang: Mapped[str] = mapped_column(String(10), nullable=False, default="es")
    
    reset_password_tokens: Mapped[List[ResetPasswordToken]] = relationship("ResetPasswordToken", back_populates="user")
    roles: Mapped[List[Role]] = relationship("Role", secondary=roles_users, back_populates="users")
    
    # Properties
        
    @property
    def is_superadmin(self) -> bool:
        return "superadmin" in self.roles_names()
    
    
    # Methods
    def to_dict(self):
        """
        Convert the User model to a dictionary
        """
        result = {}
        for c in self.__table__.columns:
            if c.name != 'password':
                value = getattr(self, c.name)
                if isinstance(value, datetime):
                    value = value.isoformat()
                result[c.name] = value
        for role in self.roles:
            result["roles"] = [
                {
                    "id": role.id,
                    "name": role.name,
                    "permissions": [permission.to_dict() for permission in role.permissions]
                }
                for role in self.roles
            ]
        return result
    
    def hash_password(self, password: str) -> str:
        return BcryptAdapter.hash(password)
    
    def check_password(self, password: str) -> bool:
        return BcryptAdapter.check(password, self.password)
    
    def can(self, permission: str) -> bool:
        if any(role.name.lower().replace(" ", "") == "superadmin" for role in self.roles):
            return True
        for role in self.roles:
            for permission in role.permissions:
                if permission.name == permission:
                    return True
        return False
    
    def has_permission(self, permission: str) -> bool:
        return self.can(permission)
    
    def has_role(self, role: str) -> bool:
        return role in [r.name for r in self.roles]
    
    def has_any_role(self, roles: List[str]) -> bool:
        return any(self.has_role(role) for role in roles)
    
    def roles_names(self) -> List[str]:
        return [role.name.lower().replace(" ", "") for role in self.roles]
    
    def companies_ids(self) -> List[int]:
        return [company.id for company in self.companies]
    
    def has_company(self, company_id: int) -> bool:
        companies_ids = self.companies_ids()
        if not companies_ids:
            return False
        return company_id in companies_ids
