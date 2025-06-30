from pydantic import BaseModel

class RoleDeleteMany(BaseModel):
    ids: list[int]
