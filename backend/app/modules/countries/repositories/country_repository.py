from app.modules.countries.models.country_model import Country
from app.modules.common.repositories.base_repository import BaseRepository
from sqlalchemy.orm import Session

class CountryRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(db, Country)
        
    
    def get_by_name(self, name: str) -> Country:
        return self.db.query(Country).filter(Country.name == name).first()