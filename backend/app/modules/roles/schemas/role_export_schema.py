from typing import Optional
from pydantic import BaseModel

class RoleExportSchema(BaseModel):
    ids: Optional[list[int]] = None
    from_date: Optional[str] = None
    to_date: Optional[str] = None