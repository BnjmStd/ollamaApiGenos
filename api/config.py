from pydantic import BaseSettings
from typing import List
from pathlib import Path
from functools import lru_cache
import json

class Settings(BaseSettings):
    # API Settings
    API_TITLE: str = "Medical Exam Processing API"
    API_DESCRIPTION: str = "API para procesar y analizar exámenes médicos"
    API_VERSION: str = "1.0.0"
    
    # Server Settings
    SERVER_HOST: str = "0.0.0.0"
    SERVER_PORT: int = 8000
    SERVER_WORKERS: int = 8
    SERVER_TIMEOUT: int = 60
    SERVER_MAX_REQUESTS: int = 1000
    SERVER_LIMIT_CONCURRENCY: int = 100
    
    # Directories
    BASE_DIR: Path = Path(__file__).parent
    RESULTS_DIR: Path = Path(__file__).parent / "results"
    TEMP_DIR: Path = Path(__file__).parent / "temp"
    LOG_FILE: Path = Path(__file__).parent / "logs" / "api.log"
    
    # CORS - valor por defecto como string JSON
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000"]
    
    # Límites y Timeouts
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    PROCESS_TIMEOUT: int = 300  # 5 minutos
    
    # Rate Limiting Settings
    RATE_LIMIT_PER_MINUTE: int = 100
    RATE_LIMIT_PER_IP: int = 1000  # límite por IP por hora
    RATE_LIMIT_WINDOW: int = 3600   # ventana de tiempo en segundos (1 hora)
    MAX_CONCURRENT_REQUESTS: int = 50  # máximo de solicitudes concurrentes
    
    # Memory Management
    MAX_MEMORY_USAGE: int = 1024 * 1024 * 1024  # 1GB en bytes
    CLEANUP_INTERVAL: int = 300  # limpieza cada 5 minutos
    
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