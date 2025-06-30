from sqlalchemy import String, ForeignKey, BIGINT, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.modules.common.models.base_model import BaseModel
from datetime import datetime, timedelta
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.modules.users.models.user_model import User

class ResetPasswordToken(BaseModel):
    __tablename__ = "reset_password_tokens"


    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    token: Mapped[str] = mapped_column(String(255), nullable=False)
    user_id: Mapped[int] = mapped_column(BIGINT, ForeignKey("users.id"), nullable=False)
    expires_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False)

    user: Mapped["User"] = relationship(back_populates="reset_password_tokens")

    def is_expired(self) -> bool:
        """Check if the token is expired"""
        return datetime.now() > self.expires_at

    @staticmethod
    def calculate_expiry(minutes: int = 10) -> datetime:
        """Calculate expiry time from now"""
        return datetime.now() + timedelta(minutes=minutes)
