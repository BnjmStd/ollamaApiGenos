# chat/monitoring.py
import psutil
from typing import Dict
import time

class ResourceMonitor:
    def __init__(self):
        self.request_count = 0
        self.error_count = 0
        self.request_timestamps: Dict[str, list] = {}
        self.requests_per_minute = 60

    def check_rate_limit(self, client_id: str) -> bool:
        now = time.time()
        if client_id not in self.request_timestamps:
            self.request_timestamps[client_id] = []

        # Limpiar timestamps antiguos
        self.request_timestamps[client_id] = [
            ts for ts in self.request_timestamps[client_id]
            if now - ts < 60
        ]

        if len(self.request_timestamps[client_id]) >= self.requests_per_minute:
            return False

        self.request_timestamps[client_id].append(now)
        return True

    def increment_request(self):
        self.request_count += 1

    def increment_error(self):
        self.error_count += 1

    async def get_metrics(self) -> dict:
        process = psutil.Process()
        return {
            "requests": self.request_count,
            "errors": self.error_count,
            "memory_usage": process.memory_info().rss,
            "cpu_percent": process.cpu_percent()
        }