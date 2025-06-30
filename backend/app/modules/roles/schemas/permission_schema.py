from datetime import datetime
from pydantic import BaseModel as BaseSchema

class PermissionSchema(BaseSchema):
    id: int
    name: str
    created_at: datetime
    updated_at: datetime
