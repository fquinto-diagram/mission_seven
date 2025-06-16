from app.modules.roles.schemas.permission_schema import PermissionSchema
from app.modules.common.schemas.pagination_schema import PaginationSchema

class PermissionResponseSchema(PaginationSchema):
    data: list[PermissionSchema]