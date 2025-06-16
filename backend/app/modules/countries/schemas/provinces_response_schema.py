from pydantic import BaseModel
from app.modules.countries.schemas.province_schema import ProvinceSchema

class ProvincesResponseSchema(BaseModel):
    data: list[ProvinceSchema]