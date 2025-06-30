from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
from typing import List
import os

load_dotenv()

def get_available_languages() -> List[str]:
    translations_dir = os.path.join(os.path.dirname(__file__), "translations")
    return [os.path.splitext(f)[0] for f in os.listdir(translations_dir) if f.endswith('.json')]

class Settings(BaseSettings):
    # App settings
    PROJECT_NAME: str = os.getenv("PROJECT_NAME")
    PROJECT_URL: str
    FRONTEND_URL: str
    PROJECT_VERSION: str
    PROJECT_DESCRIPTION: str
    DEFAULT_LANGUAGE: str = "es"
    AVAILABLE_LANGUAGES: List[str] = get_available_languages()
    PROJECT_PAGINATION_LIMIT: int = int(os.getenv("PROJECT_PAGINATION_LIMIT"))
    PROJECT_CHUNK_SIZE: int = int(os.getenv("PROJECT_CHUNK_SIZE", "100"))
    
    # Database settings
    DATABASE_URL: str
    DEBUG: bool = True
    
    # JWT settings
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    
    # Redis settings
    REDIS_URL: str = os.getenv("REDIS_URL")
    REDIS_HOST: str = os.getenv("REDIS_HOST", "redis")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_DB: int = int(os.getenv("REDIS_DB", "0"))
    REDIS_PASSWORD: str = os.getenv("REDIS_PASSWORD")
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

# Inicializar settings como None
settings = None

def get_settings() -> Settings:
    global settings
    if settings is None:
        settings = Settings()
    return settings
