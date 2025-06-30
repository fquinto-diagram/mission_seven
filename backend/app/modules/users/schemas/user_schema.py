from pydantic import BaseModel, EmailStr, Field
from app.config.translations.i18n import get_translation

class UserSchema(BaseModel):
    email: EmailStr = Field(..., description=get_translation("validation.required_field", field="email")) 