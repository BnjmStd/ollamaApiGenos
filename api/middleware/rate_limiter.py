# middleware/rate_limiter.py
# curl http://localhost:8080/rate-limit-status 
from collections import defaultdict
import time
from threading import Lock
import psutil
from fastapi import HTTPException, Request
from typing import Dict, List
from config import get_settings

settings = get_settings()

class MemoryRateLimiter:
    def __init__(self):
        self.requests: Dict[str, List[float]] = defaultdict(list)
        self.concurrent_requests: int = 0
        self.lock = Lock()
        self.last_cleanup: float = time.time()
    
    async def check_rate_limit(self, request: Request):
        """
        Verifica límites de velocidad y recursos
        """
        ip = request.client.host
        current_time = time.time()
        
        with self.lock:
            # Limpiar solicitudes antiguas
            if current_time - self.last_cleanup >= settings.CLEANUP_INTERVAL:
                self._cleanup_old_requests()
            
            # Verificar límite por IP
            recent_requests = [
                req_time for req_time in self.requests[ip]
                if current_time - req_time < 60  # último minuto
            ]
            
            if len(recent_requests) >= settings.RATE_LIMIT_PER_MINUTE:
                raise HTTPException(
                    status_code=429,
                    detail="Rate limit exceeded. Please try again later."
                )
            
            # Registrar nueva solicitud
            self.requests[ip].append(current_time)
            self.concurrent_requests += 1
            
            # Verificar memoria
            if psutil.Process().memory_info().rss > settings.MAX_MEMORY_USAGE:
                self.concurrent_requests -= 1
                raise HTTPException(
                    status_code=503,
                    detail="Server is experiencing high memory usage. Please try again later."
                )
    
    def _cleanup_old_requests(self):
        """Limpia solicitudes antiguas"""
        current_time = time.time()
        for ip in list(self.requests.keys()):
            self.requests[ip] = [
                req_time for req_time in self.requests[ip]
                if current_time - req_time < settings.RATE_LIMIT_WINDOW
            ]
            if not self.requests[ip]:
                del self.requests[ip]
        self.last_cleanup = current_time