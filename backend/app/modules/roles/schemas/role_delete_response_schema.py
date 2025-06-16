from app.modules.roles.schemas.roles_response_schema import RolesResponseSchema

class RoleDeleteResponseSchema(RolesResponseSchema):
    message: str
