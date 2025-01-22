from pydantic import BaseSettings
from typing import List
from pathlib import Path
from functools import lru_cache
import json

class Settings(BaseSettings):
    # Mantener configuraciones existentes pero remover referencias al chat
    API_TITLE: str = "Medical Exam Processing API"
    API_DESCRIPTION: str = "API para procesar y analizar exámenes médicos"
    API_VERSION: str = "1.0.0"
    
    SERVER_HOST: str = "0.0.0.0"
    SERVER_PORT: int = 8000
    SERVER_WORKERS: int = 8
    SERVER_TIMEOUT: int = 60
    SERVER_MAX_REQUESTS: int = 1000
    SERVER_LIMIT_CONCURRENCY: int = 100
    
    BASE_DIR: Path = Path(__file__).parent
    RESULTS_DIR: Path = BASE_DIR / "results"
    TEMP_DIR: Path = BASE_DIR / "temp"
    LOG_FILE: Path = BASE_DIR / "logs" / "api.log"
    
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000"]
    MAX_FILE_SIZE: int = 10 * 1024 * 1024
    PROCESS_TIMEOUT: int = 300
    
    RATE_LIMIT_PER_MINUTE: int = 100
    RATE_LIMIT_PER_IP: int = 1000
    RATE_LIMIT_WINDOW: int = 3600
    MAX_CONCURRENT_REQUESTS: int = 50
    
    MAX_MEMORY_USAGE: int = 1024 * 1024 * 1024
    CLEANUP_INTERVAL: int = 300
    
    class Config:
        env_file = ".env"
        case_sensitive = True

        @classmethod
        def parse_env_var(cls, field_name: str, raw_val: str):
            if field_name == "ALLOWED_ORIGINS":
                return json.loads(raw_val)
            return raw_val

@lru_cache()
def get_settings() -> Settings:
    return Settings()