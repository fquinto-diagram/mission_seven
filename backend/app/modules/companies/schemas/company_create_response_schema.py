from app.modules.common.schemas.base_schema import BaseSchema
from app.modules.companies.schemas.company_schema import CompanySchema

class CompanyCreateResponseSchema(BaseSchema):
    message: str
    company: CompanySchema