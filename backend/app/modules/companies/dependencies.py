from app.modules.companies.repositories.company_repository import CompanyRepository
from sqlalchemy.orm import Session
from fastapi import Depends
from app.config.database import get_db


def get_company_repository(db: Session = Depends(get_db)) -> CompanyRepository:
    return CompanyRepository(db)