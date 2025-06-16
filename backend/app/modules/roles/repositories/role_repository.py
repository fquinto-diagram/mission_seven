from app.modules.common.repositories.base_repository import BaseRepository
from app.modules.roles.models.role_model import Role
from sqlalchemy.orm import Session
from app.modules.roles.models.permission_model import Permission
from pydantic import BaseModel as BaseSchema
from app.modules.common.helpers.model_helper import update_model_attributes

class RoleRepository(BaseRepository[Role]):
    def __init__(self, db: Session):
        super().__init__(db, Role)


    def create(self, input: BaseSchema) -> Role:
        """
        Create a new role
        
        Args:
            input (BaseModel): The input to create the role with
            
        Returns:
            Role: The created role
        """
        input = input.model_dump(exclude_unset=True)
        nameInput = { "name": input["name"] }
        restored_item = super()._handle_unique_fields(nameInput)
        if restored_item:
            self.add_permissions(restored_item.id, input["permissions"])
            return restored_item
        role = self.model(**nameInput)
        self.db.add(role)
        self.db.commit()
        role = self.add_permissions(role.id, input["permissions"])
        return role
    
    def update(self, id: int, input: BaseSchema) -> Role:
        """
        Update a role
        
        Args:
            id (int): The id of the role to update
            input (BaseModel): The input to update the role with
            
        Returns:
            Role: The updated role
        """
        input = input.model_dump(exclude_unset=True)
        nameInput = { "name": input["name"] }
        super()._validate_unique_fields(nameInput, id)
        role = self.find(id)
        update_model_attributes(role, nameInput)
        self.db.commit()
        role = self.add_permissions(role.id, input["permissions"])
        return role
    
    def add_permissions(self, role_id: int, permissions: list[int]) -> None:
        """
        Add permissions to a role
        
        Args:
            role_id (int): The id of the role
            permissions (list[int]): The ids of the permissions to add
        """
        role = self.find(role_id)
        role.permissions.clear()
        for permission in permissions:
            if permission_item := self.db.query(Permission).filter(Permission.id == permission).first():
                role.permissions.append(permission_item)
        self.db.commit()
        self.db.refresh(role)
        return role
