from pydantic import BaseModel, EmailStr, Field
from app.config.translations.i18n import get_translation

class LoginRequest(BaseModel):
    email: EmailStr = Field(..., description=get_translation("validation.required_field", locale='es', field="email"))
    password: str = Field(..., min_length=8, max_length=50, description=get_translation("validation.required_field", locale='es', field="password")) 