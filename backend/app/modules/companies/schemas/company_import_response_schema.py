from pydantic import BaseModel

class CompanyImportResponseSchema(BaseModel):
    message: str