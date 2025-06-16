from fastapi import Request
from app.config.settings import get_settings
from app.modules.auth.dependencies import protected_route, get_user_repository
from app.config.database import get_db

settings = get_settings()

async def get_locale(request: Request) -> str:
    """
    Get the locale from the header or the logged in user
    """
    locale_header = request.headers.get("locale", "")
    locale = locale_header.split(",")[0].split("-")[0] if locale_header else ""
    
    if not locale:
        try:
            auth_header = request.headers.get("Authorization")
            if auth_header and auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]
                db = next(get_db())
                user_repository = get_user_repository(db)
                current_user = protected_route(token=token, user_repository=user_repository)
                if current_user and hasattr(current_user, 'lang'):
                    locale = current_user.lang
        except Exception as e:
            pass
    
    # If there is no valid locale, use the default
    if locale not in settings.AVAILABLE_LANGUAGES:
        locale = settings.DEFAULT_LANGUAGE
        
    return locale 