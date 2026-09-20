from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    ENVIRONMENT: str = "development"
    PROJECT_NAME: str = "AGENTX AI Resume Platform"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "default_secret_key_change_in_production_min_32_characters"

    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "agentx_admin"
    POSTGRES_PASSWORD: str = "agentx_secure_password"
    POSTGRES_DB: str = "agentx_db"
    DATABASE_URL: str = Field(
        default="sqlite+aiosqlite:///./app.db"
    )

    DEFAULT_LLM_PROVIDER: str = "gemini"
    GOOGLE_GEMINI_API_KEY: str = ""
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""

    UPLOAD_STORAGE_PATH: str = "./uploads"
    MAX_FILE_SIZE_BYTES: int = 10485760

    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]

    model_config = SettingsConfigDict(case_sensitive=True, env_file=".env", extra="ignore")


settings = Settings()
