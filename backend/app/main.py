import uvicorn
import logging
from fastapi import FastAPI, Request, WebSocket, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.config.settings import get_settings
from app.modules.common.router import router
from app.config.translations.i18n import get_translation, set_locale
from app.config.translations.locale import get_locale
from app.config.log import setup_logger
from app.config.websocket import websocket_broadcaster
from app.modules.users.repositories.user_repository import UserRepository
from app.config.database import SessionLocal
from fastapi import WebSocketDisconnect
from app.adapters.log_adapter import LogAdapter
from app.modules.common.scopes import before_compile # Apply the company scope to all queries

settings = get_settings()
logger = logging.getLogger(__name__)


app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.PROJECT_VERSION,
    openapi_url=f"/openapi.json"
)

# Set CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

setup_logger()

@app.websocket("/ws/jobs/{job_id}")
async def websocket_job_progress(websocket: WebSocket, job_id: str):
    locale = settings.DEFAULT_LANGUAGE
    
    try:
        protocols = websocket.headers.get("sec-websocket-protocol", "").split(",")
        
        token_protocol = next((p.strip() for p in protocols if p.strip().startswith("token.")), None)
        locale_protocol = next((p.strip() for p in protocols if p.strip().startswith("locale.")), None)
        
        if not token_protocol and not locale_protocol:
            await websocket.close(code=1008, reason=get_translation("errors.unauthorized", settings.DEFAULT_LANGUAGE))
            return
            
        if locale_protocol:
            await websocket.accept(subprotocol=locale_protocol)
            locale = locale_protocol.replace("locale.", "") if locale_protocol else settings.DEFAULT_LANGUAGE
            
            try:
                await websocket_broadcaster(websocket, job_id)
            except WebSocketDisconnect:
                pass
            except Exception as e:
                LogAdapter.error(f"Error in websocket_broadcaster: {str(e)}")
                try:
                    await websocket.close(code=1011, reason=get_translation("errors.internal_server_error", locale))
                except:
                    pass
            return
            
        token = token_protocol.replace("token.", "")
        
        try:
            db = SessionLocal()
            user_repository = UserRepository(db)
            try:
                user = user_repository.get_by_token(token)
                if not user:
                    await websocket.close(code=1008, reason=get_translation("errors.unauthorized", locale))
                    return
                    
                if f"user-{user.id}" != job_id:
                    await websocket.close(code=1008, reason=get_translation("errors.unauthorized", locale))
                    return
                
                await websocket.accept(subprotocol=token_protocol)
                
                try:
                    await websocket_broadcaster(websocket, job_id)
                except WebSocketDisconnect:
                    pass
                except Exception as e:
                    try:
                        await websocket.close(code=1011, reason=get_translation("errors.internal_server_error", locale))
                    except:
                        pass
            finally:
                db.close()
                    
        except Exception as e:
            await websocket.close(code=1008, reason=get_translation("errors.unauthorized", locale))
            
    except Exception as e:
        try:
            await websocket.close(code=1011, reason=get_translation("errors.internal_server_error", locale))
        except:
            pass


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Global handler to translate validation errors
    """
    # Get the locale from the header or the user
    locale = await get_locale(request)
    set_locale(locale)
    
    errors = exc.errors()
    for err in errors:
        error_type = err["type"].split(".")
        field_name = err["loc"][-1]
        
        translated_field = get_translation(f"attributes.{field_name}", locale)
        
        # Prepare the context with all the necessary data
        ctx = err.get("ctx", {})
        ctx["field"] = translated_field
        if "input" in err:
            ctx["input"] = err["input"]
            # For email errors, use the input as the email value
            if field_name == "email":
                ctx["email"] = err["input"]
        
        # Determine the translation key according to the error type
        if error_type[0] == "string_too_short":
            translation_key = "validation.field_min_length"
        elif error_type[0] == "string_too_long":
            translation_key = "validation.field_max_length"
        elif error_type[0] == "value_error" and field_name == "email":
            translation_key = "validation.value_error.email"
        else:
            # For other types of error, build the hierarchical key
            translation_key = "validation"
            for part in error_type:
                translation_key = f"{translation_key}.{part}"
        
        translated_msg = get_translation(translation_key, locale, **ctx)
        
        # If the translation is not found, try with a generic message
        if translated_msg == translation_key:
            generic_key = "validation.field_must_be_valid"
            translated_msg = get_translation(generic_key, locale, **ctx)
            if translated_msg == generic_key:
                translated_msg = f"El campo {translated_field} no es válido"
        
        try:
            err["msg"] = translated_msg.format(**ctx)
        except (KeyError, ValueError):
            err["msg"] = translated_msg
    
    return JSONResponse(
        status_code=422,
        content={"detail": errors}
    )

# Include routes
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 