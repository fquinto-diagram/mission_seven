from fastapi import Depends
from app.modules.countries.repositories.country_repository import CountryRepository
from app.config.database import get_db
from sqlalchemy.orm import Session
from app.modules.countries.repositories.province_repository import ProvinceRepository

def get_country_repository(db: Session = Depends(get_db)):
    return CountryRepository(db)

def get_province_repository(db: Session = Depends(get_db)):
    return ProvinceRepository(db)