from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "MediLink"
    MONGO_URI: str = "mongodb://localhost:27017"
    MONGO_DB: str = "medilink"

    class Config:
        env_file = ".env"   # so you can keep secrets in .env
        env_file_encoding = "utf-8"

settings = Settings()
