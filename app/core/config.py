
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    FIREBASE_CREDENTIALS_PATH: str
    APP_ENV:   str  = "development"
    APP_TITLE: str  = "Tutoring API"
    APP_VERSION: str = "1.0.0"

    class Config:
        env_file = ".env"


settings = Settings()
