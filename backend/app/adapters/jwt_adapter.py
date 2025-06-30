from jose import jwt, JWTError
from datetime import datetime, timedelta
from app.config.translations.i18n import get_translation
from app.config.settings import get_settings
from app.libraries.http.exception_library import ExceptionLibrary
from app.libraries.date_formatter import DateFormatter

class JwtAdapter:
    
    def __init__(self):
        settings = get_settings()
        self.secret_key = settings.SECRET_KEY
        self.algorithm = settings.ALGORITHM
        self.expire_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES

    def create_access_token(self, data: dict):
        """
        Create a JWT access token for a user.

        Args:
            data (dict): User data to include in the token.

        Returns:
            tuple: Access token and expiration time.
        """
        to_encode = data.copy()
        expire = DateFormatter.current_datetime() + timedelta(minutes=self.expire_minutes)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt, expire
    
    def verify_token(self, token: str):
        """
        Check if a JWT token is valid.

        Args:
            token (str): JWT token to verify.

        Returns:
            dict: User data from the token.
        """
        try:
            return jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
        except JWTError:
            ExceptionLibrary.throw_401("auth.unauthenticated")
