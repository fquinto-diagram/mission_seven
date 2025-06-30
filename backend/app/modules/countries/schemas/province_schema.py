from pydantic import BaseModel
from datetime import datetime

class ProvinceSchema(BaseModel):
    id: int
    name: str
    country_id: int
    postcode: str
    created_at: datetime
    updated_at: datetime
    