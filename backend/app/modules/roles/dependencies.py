from fastapi import Depends
from app.config.database import get_db
from app.modules.roles.repositories.role_repository import RoleRepository
from app.modules.roles.repositories.permissions_repository import PermissionsRepository
from sqlalchemy.orm import Session

def get_role_repository(db: Session = Depends(get_db)) -> RoleRepository:
    return RoleRepository(db)

def get_permissions_repository(db: Session = Depends(get_db)) -> PermissionsRepository:
    return PermissionsRepository(db)