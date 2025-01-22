from pydantic import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    OLLAMA_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama2"
    CHAT_HOST: str = "0.0.0.0" 
    CHAT_PORT: int = 8001
    MAX_CONNECTIONS: int = 10000
    CONNECTION_TIMEOUT: int = 600
    RATE_LIMIT_PER_MIN: int = 60
    CHAT_WORKERS: int = 4

    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings()