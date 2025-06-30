from app.modules.common.schemas.base_schema import BaseSchema
from pydantic import Field

class CompanyExportSchema(BaseSchema):
    ids: list[int] = Field(default=[])
    from_date: str = Field(default="")
    to_date: str = Field(default="")