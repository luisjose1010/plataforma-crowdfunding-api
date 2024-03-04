import os
import logging
from dotenv import load_dotenv

from pathlib import Path
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# Eliminar una alerta la alerta que ocurre por la version de bcrypt con respecto a passlib
logging.getLogger('passlib').setLevel(logging.ERROR)

class Settings:
    PROJECT_NAME:str = "Plataforma Crowdfunding"
    PROJECT_VERSION: str = "1.0.0"

    POSTGRES_USER : str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_SERVER : str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_PORT : str = os.getenv("POSTGRES_PORT", 5432) # default postgres port is 5432
    POSTGRES_DB : str = os.getenv("POSTGRES_DB", "plataforma-crowfunding")
    DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"

    SECRET_KEY : str = os.getenv("SECRET_KEY")
    ACCESS_TOKEN_EXPIRE_MINUTES : int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 1440)) # 24 Horas
    ALGORITHM : str = "HS256"

    SERVER_APP: str = "main:app"
    SERVER_HOST: str = os.getenv("SERVER_HOST", "127.0.0.1")
    SERVER_PORT: int = int(os.getenv("SERVER_PORT", 8000))
    SERVER_RELOAD: bool = bool(os.getenv("SERVER_RELOAD", True))
    SERVER_LOG_LEVEL: str = os.getenv("SERVER_LOG_LEVEL", "debug")

    CORS_ORIGIN : str = os.getenv("CORS_ORIGIN", "*")

settings = Settings()