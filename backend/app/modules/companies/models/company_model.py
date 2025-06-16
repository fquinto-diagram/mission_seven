from app.modules.common.models.base_model import BaseModel, SoftDeleteMixin
from sqlalchemy import BIGINT, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.schema import ForeignKey
from sqlalchemy.orm import relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.modules.countries.models.country_model import Country



class Company(BaseModel, SoftDeleteMixin):
    SEARCH_FIELDS = ["legal_name", "trade_name", "cif", "email"]
    DEFAULT_ORDER_BY = "legal_name"
    
    __tablename__ = "companies"
    
    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, index=True, autoincrement=True)
    legal_name: Mapped[str] = mapped_column(String(40), unique=True, index=True, nullable=False)
    trade_name: Mapped[str] = mapped_column(String(40), unique=True, index=True, nullable=False)
    cif: Mapped[str] = mapped_column(String(15), unique=True, index=True)
    address: Mapped[str] = mapped_column(String(50), nullable=False)
    country_id: Mapped[int] = mapped_column(BIGINT, ForeignKey("countries.id"), nullable=False)
    province: Mapped[str] = mapped_column(String(100), nullable=False)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    phone: Mapped[str] = mapped_column(String(15), nullable=True)
    web: Mapped[str] = mapped_column(String(100), nullable=True)
    email: Mapped[str] = mapped_column(String(100), nullable=False)
    
    country: Mapped["Country"] = relationship("Country", back_populates="companies")