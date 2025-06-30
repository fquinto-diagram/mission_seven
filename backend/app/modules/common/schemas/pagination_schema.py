from pydantic import BaseModel as BaseSchema
from typing import Optional
import os


class PaginationSchema(BaseSchema):
    page: Optional[int] = 1
    limit: Optional[int] = int(os.getenv("PROJECT_PAGINATION_LIMIT"))
    total: Optional[int] = 0
    total_pages: Optional[int] = 0
    data: list = []
