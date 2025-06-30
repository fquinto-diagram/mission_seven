from typing import Optional
from fastapi import Query

class RoleFilter:
    def __init__(
        self,
        limit: int = 0,
        page: int = 1,
        search: str = "",
        include: Optional[list[str]] = Query(None, alias="include[]")
    ):
        self.limit = limit
        self.page = page
        self.search = search
        self.include = include

