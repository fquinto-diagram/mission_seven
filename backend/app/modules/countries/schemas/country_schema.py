from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CountrySchema(BaseModel):
    id: int
    name: str
    iso_2_code: str
    iso_3_code: str
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None