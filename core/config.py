from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import (
    AnyUrl,
    BeforeValidator,
)
from typing import Annotated, Any

def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "User Mgmt"
    FIRESTORE_JSON_PATH: str
    FIRESTORE_COLLECTION_NAME: str
    EMAIL_USER: str
    EMAIL_PASSWORD: str
    SMTP_HOST: str
    SMTP_PORT: str
    

    BACKEND_CORS_ORIGINS: Annotated[
        list[AnyUrl] | str, BeforeValidator(parse_cors)
    ] = []

settings = Settings()