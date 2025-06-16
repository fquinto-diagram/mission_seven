from fastapi import APIRouter
from app.modules.countries.repositories.country_repository import CountryRepository
from fastapi import Depends
from app.modules.countries.dependencies import get_country_repository, get_province_repository
from app.modules.countries.schemas.country_filter_schema import CountryFilter
from app.modules.countries.repositories.province_repository import ProvinceRepository
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from app.modules.users.models.user_model import User
from app.modules.auth.dependencies import protected_route
from app.modules.countries.schemas.countries_response_schema import CountriesResponseSchema
from app.modules.countries.schemas.provinces_response_schema import ProvincesResponseSchema

router = APIRouter(prefix="/countries", tags=["countries"])

@router.get("", response_model=CountriesResponseSchema)
async def get_countries(query: CountryFilter = Depends(), user: User = Depends(protected_route), country_repository: CountryRepository = Depends(get_country_repository)):
    countries = country_repository.list(query)
    return JSONResponse(
        status_code=200, 
        content=jsonable_encoder(countries)
    )
    
@router.get("/{country_id}/provinces", response_model=ProvincesResponseSchema)
async def get_provinces(country_id: int, user: User = Depends(protected_route), province_repository: ProvinceRepository = Depends(get_province_repository)):
    provinces = { "data": province_repository.get_by_country_id(country_id)}
    return JSONResponse(
        status_code=200, 
        content=jsonable_encoder(provinces)
    )