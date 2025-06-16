from sqlalchemy.orm import Session
from app.modules.auth.models.reset_password_token_model import ResetPasswordToken

class ResetPasswordTokenRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, token: str, user_id: int) -> ResetPasswordToken:
        reset_token = ResetPasswordToken(token=token, user_id=user_id)
        self.db.add(reset_token)
        self.db.commit()
        self.db.refresh(reset_token)
        return reset_token

    def get_by_token(self, token: str) -> ResetPasswordToken:
        return self.db.query(ResetPasswordToken).filter(ResetPasswordToken.token == token).first()

    def delete(self, token: str) -> None:
        self.db.query(ResetPasswordToken).filter(ResetPasswordToken.token == token).delete()
        self.db.commit()
