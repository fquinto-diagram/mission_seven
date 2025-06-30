from fastapi import Header, APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
import bcrypt
from app.modules.users.repositories.user_repository import UserRepository
from app.modules.auth.dependencies import get_user_repository
from app.config.translations.i18n import get_translation
from app.adapters.jwt_adapter import JwtAdapter
from app.modules.auth.schemas import ResetPasswordEmailRequest, ResetPasswordRequest
from app.modules.users.schemas import LoginRequest, UpdateProfileRequest, UpdatePasswordRequest
from app.adapters.mail_adapter import MailAdapter
import os
from app.modules.auth.repositories.reset_password_token_repository import ResetPasswordTokenRepository
from app.modules.auth.dependencies import get_reset_password_token_repository
from app.libraries.http.exception_library import ExceptionLibrary
from app.modules.auth.dependencies import protected_route
from app.modules.users.models import User
from app.adapters.log_adapter import LogAdapter
router = APIRouter(prefix="", tags=["auth"])

@router.post("/login")
async def login(
    login_data: LoginRequest, 
    user_repository: UserRepository = Depends(get_user_repository),
    locale: str = Header(default="es")
):
    try:
        user = user_repository.get_by_email(login_data.email)
        
        ExceptionLibrary.throw_404(user, "auth.invalid_credentials", locale)
            
        try:
            password_match = bcrypt.checkpw(
                login_data.password.encode('utf-8'), 
                user.password.encode('utf-8')
            )
        except (ValueError, TypeError) as e:
            ExceptionLibrary.throw_401("auth.invalid_credentials", locale)
        
        ExceptionLibrary.throw_401_if(not password_match, "auth.invalid_credentials", locale)
        
        jwt = JwtAdapter()
        token, expire = jwt.create_access_token({"user_id": user.id})
        
        return JSONResponse(
            content={
                "user": user.to_dict(),
                "token": token,
                "expiresAt": expire.isoformat()
            }
        )
    except HTTPException as e:
        ExceptionLibrary.throw_400(e.detail, locale)
    except Exception as e:
        LogAdapter.error('Error in login: ', { "error": str(e) })
        ExceptionLibrary.throw_500_if(True, "errors.internal_server_error", locale)
        
@router.post("/reset-password-email")
async def reset_password_email(base: ResetPasswordEmailRequest, user_repository: UserRepository = Depends(get_user_repository), locale: str = Header(default="es")):
    user = user_repository.get_by_email(base.email)
    
    ExceptionLibrary.throw_404(user, "users.not_found", locale)
        
    token = user_repository.generate_password_reset_token(user.id)
    
    try:
        mail = MailAdapter(user.lang)
        isSent = await mail.send_email(
            template=os.path.join("auth", "reset-password.html"),
            to=str(user.email),
            body={
                "token": token,
                "name": user.name,
            },
            subject=get_translation("auth.password_reset_subject", user.lang),
        )
        ExceptionLibrary.throw_400_if(not isSent, "errors.email_not_sent", locale)
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": get_translation("auth.password_reset_email_sent", user.lang)})
    except HTTPException as e:
        ExceptionLibrary.throw_400("errors.email_not_sent", locale)
        raise e
    except Exception as e:
        ExceptionLibrary.throw_500_if(True, "errors.internal_server_error", locale)
  
@router.post("/reset-password")
async def reset_password(request: ResetPasswordRequest, user_repository: UserRepository = Depends(get_user_repository), reset_password_token_repository: ResetPasswordTokenRepository = Depends(get_reset_password_token_repository), locale: str = Header(default="es")):
    user = user_repository.get_by_reset_password_token(request.token)
    ExceptionLibrary.throw_404(user, "errors.invalid_token", locale)
    reset_password_token_repository.delete(request.token)
    user_repository.update_password(user.id, user.hash_password(request.password))
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": get_translation("auth.password_reset_success", locale)})

@router.get("/profile")
async def profile(user: User = Depends(protected_route)):
    return JSONResponse(status_code=status.HTTP_200_OK, content={ "user": user.to_dict() })

@router.put("/profile")
async def update_profile(request: UpdateProfileRequest, user: User = Depends(protected_route), user_repository: UserRepository = Depends(get_user_repository), locale: str = Header(default="es")):
    newUser = user_repository.get_by_email(request.email)  
    ExceptionLibrary.throw_400_if(not user_repository.is_same_user(user, newUser), "auth.email_already_registered", locale)
    user_repository.update(user.id, request)        
    return JSONResponse(status_code=status.HTTP_200_OK, content={ "user": user.to_dict(), "message": get_translation("auth.profile_updated", user.lang) })


@router.patch("/profile/password")
async def update_password(request: UpdatePasswordRequest, user: User = Depends(protected_route), user_repository: UserRepository = Depends(get_user_repository), locale: str = Header(default="es")):
    ExceptionLibrary.throw_400_if(not user.check_password(request.password), "auth.invalid_password", locale)
    user_repository.update_password(user.id, user.hash_password(request.new_password))
    return JSONResponse(status_code=status.HTTP_200_OK, content={ "message": get_translation("auth.password_updated", user.lang) })


