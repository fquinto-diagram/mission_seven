from app.modules.roles.models.permission_model import Permission
from app.modules.common.repositories.base_repository import BaseRepository
from sqlalchemy.orm import Session

class PermissionsRepository(BaseRepository[Permission]):
    def __init__(self, db: Session):
        super().__init__(db, Permission)
