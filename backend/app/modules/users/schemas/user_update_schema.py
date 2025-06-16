from pydantic import BaseModel, EmailStr, Field
from app.config.translations.i18n import get_translation

class UserUpdate(BaseModel):
    name: str = Field(..., max_length=50, description=get_translation("validation.required_field", locale='es', field="name"))
    surname: str = Field(..., max_length=100, description=get_translation("validation.required_field", locale='es', field="surname"))
    email: EmailStr = Field(..., max_length=100, description=get_translation("validation.required_field", locale='es', field="email"))
    lang: str = Field(..., min_length=2, max_length=10, description=get_translation("validation.required_field", locale='es', field="lang"))

class UpdateProfileRequest(UserUpdate):
    pass 