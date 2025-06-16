from app.modules.countries.schemas.country_schema import CountrySchema
from app.modules.common.schemas.pagination_schema import PaginationSchema

class CountriesResponseSchema(PaginationSchema):
    data: list[CountrySchema]