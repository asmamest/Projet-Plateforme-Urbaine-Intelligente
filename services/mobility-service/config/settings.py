"""
Configuration centralisée de l'application
"""
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Service Mobilité Intelligente"
    app_version: str = "1.0.0"
    debug: bool = True
    host: str = "0.0.0.0"
    port: int = 8000
    
    class Config:
        env_file = ".env"

settings = Settings()
