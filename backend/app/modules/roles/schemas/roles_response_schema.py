from app.modules.common.schemas.pagination_schema import PaginationSchema
from app.modules.roles.schemas.role_schema import RoleSchema

class RolesResponseSchema(PaginationSchema):
    data: list[RoleSchema]