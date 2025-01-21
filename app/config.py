from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MODE: Literal["DEV", "TEST", "PROD"]
    LOG_LEVEL: Literal[
        "TRACE", "DEBUG", "INFO", 
        "WARN", "ERROR", "FATAL"
    ]
    
    FASTAPI_HOST: str
    FASTAPI_PORT: int

    DB_HOST : str
    DB_PORT : int
    DB_USER : str
    DB_PASS : str
    DB_NAME : str
    DB_DRIVER : str
    DATABASE_URL : str

    TEST_DB_HOST : str
    TEST_DB_PORT : int
    TEST_DB_USER : str
    TEST_DB_PASS : str
    TEST_DB_NAME : str
    TEST_DATABASE_URL : str

    SMTP_HOST : str
    SMTP_PORT : int
    SMTP_USER : str
    SMTP_PASS : str

    REDIS_HOST : str
    REDIS_PORT : int

    SECRET_KEY : str
    HASH_ALGO : str

    model_config = SettingsConfigDict(env_file='.env')    


settings = Settings()