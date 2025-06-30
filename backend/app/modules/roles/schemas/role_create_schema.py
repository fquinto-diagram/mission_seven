from app.modules.roles.schemas.role_schema import RoleSchema
from pydantic import Field

class RoleCreate(RoleSchema):
    name: str = Field(..., min_length=3, max_length=255, description="Name of the role")
    permissions: list[int]