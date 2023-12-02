from pydantic import ConfigDict, field_validator
from pydantic_settings import BaseSettings
from typing import ClassVar, List, Optional, Union
from pathlib import Path


class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env", extra="forbid")

    # env variables
    LOG_LEVEL: str

    # mongodb
    MONGODB_HOST: str
    MONGODB_PORT: int
    MONGODB_DATABASE: str
    MONGODB_USERNAME: str
    MONGODB_PASSWORD: str
    MONGODB_EXPOSE_PORT: int

    # Security
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    JWT_TOKEN_PREFIX: str

    UPLOAD_DIR: str = "/uploads"
    # project config
    PROJECT_NAME: str = "Todo"
    API_V1_STR: str = "/api/"
    API_PORT: Optional[int] = 8000

    BACKEND_CORS_ORIGINS: List[str] = []

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    ENVIRONMENT: str
    ROOT_DIR: ClassVar = Path(__file__).parent.parent.parent


# init settings instance
settings = Settings()
