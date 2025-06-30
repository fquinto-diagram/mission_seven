from pydantic import EmailStr, Field, BaseModel
from app.config.translations.i18n import get_translation

class ResetPasswordEmailRequest(BaseModel):
    email: EmailStr = Field(..., max_length=100, description=get_translation('validation.required_field', field="email"))
    

class ResetPasswordRequest(BaseModel):
    token: str = Field(..., min_length=100, max_length=100, description=get_translation('validation.required_field', field="token"))
    password: str = Field(..., min_length=8, max_length=50, description=get_translation('validation.required_field', field="password"))