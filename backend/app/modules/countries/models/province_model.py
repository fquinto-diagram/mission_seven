from app.modules.common.models.base_model import BaseModel, SoftDeleteMixin
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BIGINT, String, ForeignKey
from sqlalchemy.orm import relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.modules.countries.models.country_model import Country

class Province(BaseModel, SoftDeleteMixin):
    __tablename__ = "provinces"
    
    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    country_id: Mapped[int] = mapped_column(BIGINT, ForeignKey("countries.id"), nullable=False)
    postcode: Mapped[str] = mapped_column(String(5), nullable=False)
    
    country = relationship("Country", back_populates="provinces")