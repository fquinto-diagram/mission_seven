from app.modules.common.schemas.pagination_schema import PaginationSchema
from app.modules.users.schemas.user_schema import UserSchema

class UserResponseSchema(PaginationSchema):
    data: list[UserSchema]