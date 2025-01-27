import httpx
import json
from loguru import logger
import time
from core.monitoring import ResourceMonitor
from core.config import get_settings

class OllamaService:
    def __init__(self):
        self.settings = get_settings()
        self.base_url = self.settings.OLLAMA_URL
        self.client = httpx.AsyncClient(
            timeout=httpx.Timeout(self.settings.CONNECTION_TIMEOUT, connect=5.0),
            limits=httpx.Limits(max_keepalive_connections=20, max_connections=self.settings.MAX_CONNECTIONS)
        )
        self.monitor = ResourceMonitor()
        self.monitor.requests_per_minute = self.settings.RATE_LIMIT_PER_MIN

    async def check_ollama_status(self) -> bool:
        try:
            response = await self.client.get(f"{self.base_url}/api/version")
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Ollama no está respondiendo: {e}")
            return False

    async def get_response(self, question: str, context: str = None, client_id: str = "anonymous") -> str:
        start_time = time.time()
        
        try:
            if not self.monitor.check_rate_limit(client_id):
                self.monitor.increment_error()
                return "Has excedido el límite de solicitudes por minuto. Por favor, espera un momento."

            prompt = f"""Responde basándote en el siguiente contexto. Se breve y conciso: Contexto: {context} Pregunta: {question}"""
            # Logging detallado
            logger.info("=== INICIO PROMPT ===")
            logger.info(f"Pregunta original: {question}")
            logger.info("Contexto completo:")
            logger.info(context if context else "Sin contexto")
            logger.info("Prompt final:")
            logger.info(prompt)
            logger.info("=== FIN PROMPT ===")

            try:
                response = await self.client.post(
                    f"{self.base_url}/api/generate",
                    json={
                        "model": self.settings.OLLAMA_MODEL,
                        "prompt": prompt,
                        "stream": False
                    },
                    timeout=httpx.Timeout(self.settings.CONNECTION_TIMEOUT, connect=5.0)
                )
            except httpx.TimeoutException:
                self.monitor.increment_error()
                return "La respuesta está tomando demasiado tiempo. Por favor, intenta de nuevo."
            except httpx.ConnectError:
                self.monitor.increment_error()
                return "No se pudo conectar con Ollama. Por favor, verifica que el servicio esté ejecutándose."

            if response.status_code != 200:
                self.monitor.increment_error()
                error_detail = response.text
                logger.error(f"Error de Ollama API: {response.status_code} - {error_detail}")
                return f"Error del servicio: {error_detail}"

            try:
                data = response.json()
            except json.JSONDecodeError as e:
                self.monitor.increment_error()
                logger.error(f"Error decodificando respuesta: {e}")
                return "Error procesando la respuesta del servicio."

            response_text = data.get('response')
            if not response_text:
                self.monitor.increment_error()
                return "No se obtuvo respuesta del servicio."

            self.monitor.increment_request()
            return response_text

        except Exception as e:
            self.monitor.increment_error()
            error_msg = str(e) if str(e) else "Error desconocido"
            logger.error(f"Error con Ollama: {error_msg}")
            return f"Error del servicio: {error_msg}"
        
        finally:
            duration = time.time() - start_time
            logger.info(f"Tiempo de respuesta: {duration:.2f}s")

    async def cleanup(self):
        await self.client.aclose()

    async def get_metrics(self) -> dict:
        return await self.monitor.get_metrics()