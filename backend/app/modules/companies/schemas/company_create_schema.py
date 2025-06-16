from app.modules.common.schemas.base_schema import BaseSchema
from typing import Optional
from pydantic import Field, EmailStr

class CompanyCreateSchema(BaseSchema):
    legal_name: str = Field(..., max_length=40, description="Legal name of the company")
    trade_name: str = Field(..., max_length=40, description="Trade name of the company")
    cif: str = Field(..., max_length=15, description="CIF of the company")
    address: str = Field(..., max_length=50, description="Address of the company")
    country_id: int = Field(..., description="Country id of the company")
    city: str = Field(..., max_length=100, description="City of the company")
    province: str = Field(..., max_length=100, description="Province of the company")
    phone: Optional[str] = Field(None, max_length=15, description="Phone of the company")
    email: EmailStr = Field(..., max_length=100, description="Email of the company")
    web: Optional[str] = Field(None, max_length=100, description="Web of the company")