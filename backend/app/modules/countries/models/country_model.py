from app.modules.common.models.base_model import BaseModel, SoftDeleteMixin
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BIGINT, String
from sqlalchemy.orm import relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.modules.countries.models.province_model import Province
    from app.modules.companies.models.company_model import Company


class Country(BaseModel, SoftDeleteMixin):
    __tablename__ = "countries"
    
    DEFAULT_ORDER_BY = "name"
    
    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    iso_2_code: Mapped[str] = mapped_column(String(2), nullable=False, unique=True)
    iso_3_code: Mapped[str] = mapped_column(String(3), nullable=False, unique=True)
    provinces: Mapped[list["Province"]] = relationship("Province", back_populates="country")
    companies: Mapped[list["Company"]] = relationship("Company", back_populates="country")