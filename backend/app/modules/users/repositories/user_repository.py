from sqlalchemy.orm import Session
from app.modules.users.models.user_model import User
from app.modules.users.schemas import UserUpdate
import secrets
from datetime import datetime, timedelta
from app.modules.auth.models.reset_password_token_model import ResetPasswordToken
from app.modules.common.helpers.model_helper import update_model_attributes
from app.libraries.http.exception_library import ExceptionLibrary
from app.modules.common.repositories.base_repository import BaseRepository
from app.adapters.jwt_adapter import JwtAdapter

class UserRepository(BaseRepository[User]):
    def __init__(self, db: Session):
        super().__init__(db, User)
    
    def get_by_id(self, user_id: int) -> User:
        user = self.db.query(User).filter(User.id == user_id).first()
        ExceptionLibrary.throw_404_if(not user, "users.not_found")
        return user
    
    
    def get_by_email(self, email: str, include_deleted: bool = False) -> User:
        return self.db.query(User).filter(User.email == email).filter(User.deleted_at.is_(None if not include_deleted else True)).first()
    
    def get_by_token(self, token: str) -> User:
        jwt_adapter = JwtAdapter()
        decoded_token = jwt_adapter.verify_token(token)
        return self.db.query(User).filter(User.id == decoded_token["user_id"]).first()
    
    def generate_password_reset_token(self, user_id: int) -> str:
        token = secrets.token_hex(50)
        now = datetime.now()
        self.db.add(ResetPasswordToken(
            token=token, 
            user_id=user_id, 
            expires_at=now + timedelta(minutes=15),
        ))
        self.db.commit()
        return token
    
    def get_by_reset_password_token(self, token: str) -> User:
        return self.db.query(User).join(ResetPasswordToken).filter(ResetPasswordToken.token == token).filter(ResetPasswordToken.expires_at > datetime.now()).first()
    
    def update_password(self, user_id: int, hashed_password: str) -> bool:
        user = self.get_by_id(user_id)
        ExceptionLibrary.throw_404_if(not user, "users.not_found")
        user.password = hashed_password
        self.db.commit()
        return True
    
    # def create(self, user: UserCreate) -> User:
    #     hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
    #     db_user = User(
    #         email=user.email,
    #         password=hashed_password
    #     )
    #     self.db.add(db_user)
    #     self.db.commit()
    #     self.db.refresh(db_user)
    #     return db_user
    
    def is_same_user(self, user: User, new_user: User) -> bool:
        return new_user.email == user.email and new_user.id == user.id
    
    def update(self, user_id: int, input: UserUpdate) -> User:
        db_user = self.get_by_id(user_id)
        ExceptionLibrary.throw_404_if(not db_user, "users.not_found")
        
        if hasattr(input, "password") and input.password:
            input.password = db_user.hash_password(input.password)
            
        update_data = input.model_dump(exclude_unset=True)
        update_model_attributes(db_user, update_data)
            
        self.db.commit()
        self.db.refresh(db_user)
        return db_user 