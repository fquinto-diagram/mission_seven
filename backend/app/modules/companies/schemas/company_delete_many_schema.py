from pydantic import BaseModel

class CompanyDeleteMany(BaseModel):
    ids: list[int]
