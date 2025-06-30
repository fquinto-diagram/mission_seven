from app.modules.common.schemas.base_schema import BaseSchema
from app.modules.countries.schemas.country_schema import CountrySchema
from typing import Optional

class CompanySchema(BaseSchema):
    id: int
    legal_name: str
    trade_name: str
    cif: str
    address: str
    province: str
    city: str
    phone: Optional[str] = None
    web: Optional[str] = None
    email: str
    country: Optional[CountrySchema] = None