from fastapi import Depends
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.modules.users.repositories.user_repository import UserRepository
from app.modules.auth.repositories.reset_password_token_repository import ResetPasswordTokenRepository
from app.adapters.jwt_adapter import JwtAdapter
from fastapi.security import OAuth2PasswordBearer
from app.modules.users.models.user_model import User
from app.modules.common.dependencies import get_global_company_id
from app.libraries.http.exception_library import ExceptionLibrary
from app.adapters.log_adapter import LogAdapter

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(db)

def get_reset_password_token_repository(db: Session = Depends(get_db)) -> ResetPasswordTokenRepository:
    return ResetPasswordTokenRepository(db)

def protected_route(token: str = Depends(oauth2_scheme), user_repository: UserRepository = Depends(get_user_repository)):
    jwt_adapter = JwtAdapter()
    data = jwt_adapter.verify_token(token)
    return user_repository.get_by_id(data.get("user_id"))


def protected_company_scope(user: User = Depends(protected_route)) -> User:
    company_id = get_global_company_id()
  
    if user.is_superadmin:
        return user
    
    if not user.has_company(company_id):
        LogAdapter.error(f"User {user.id} tried to access company {company_id}")
        ExceptionLibrary.throw_403("errors.unauthorized")
        
    return user