from app.modules.countries.models.province_model import Province
from app.modules.common.repositories.base_repository import BaseRepository
from sqlalchemy.orm import Session

class ProvinceRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(db, Province)
        
        
    def get_by_country_id(self, country_id: int):
        return self.db.query(Province).filter(Province.country_id == country_id).all()