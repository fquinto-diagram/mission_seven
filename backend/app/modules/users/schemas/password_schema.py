from pydantic import BaseModel, Field
from app.config.translations.i18n import get_translation

class UpdatePasswordRequest(BaseModel):
    password: str = Field(..., min_length=8, max_length=50, description=get_translation("validation.required_field", locale='es', field="password"))
    new_password: str = Field(..., min_length=8, max_length=50, description=get_translation("validation.required_field", locale='es', field="new_password")) 