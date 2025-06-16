from pydantic import BaseModel, Field

class RoleSchema(BaseModel):
    name: str = Field(..., min_length=3, max_length=255, unique=True, description="The name of the role")
