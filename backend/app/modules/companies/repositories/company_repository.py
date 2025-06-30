from app.modules.companies.models.company_model import Company
from app.modules.common.repositories.base_repository import BaseRepository
from sqlalchemy.orm import Session  


class CompanyRepository(BaseRepository[Company]):
    def __init__(self, db: Session):
        super().__init__(db, Company)
        
        
    def get_by_cif(self, cif: str) -> Company | None:
        return self.db.query(Company).filter(Company.cif == cif).first()