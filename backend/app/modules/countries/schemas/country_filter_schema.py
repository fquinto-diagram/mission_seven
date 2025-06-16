from pydantic import BaseModel

class CountryFilter:
    def __init__(
        self,
        limit: int = 0,
        page: int = 1,
        search: str = "",
        include: list[str] = []
    ):
        self.limit = limit
        self.page = page
        self.search = search
        self.include = include