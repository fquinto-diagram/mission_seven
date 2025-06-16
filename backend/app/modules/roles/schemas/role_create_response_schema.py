from app.modules.common.schemas.base_schema import BaseSchema
from app.modules.roles.schemas.role_schema import RoleSchema

class RoleCreateResponseSchema(BaseSchema):
    role: RoleSchema
    message: str
