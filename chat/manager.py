from fastapi import WebSocket
from typing import Dict
import base64
from PyPDF2 import PdfReader
from io import BytesIO
from loguru import logger
import time

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.pdf_contents: Dict[str, str] = {}
        self.max_connections = 10000
        self.connection_timeout = 600

    async def connect(self, websocket: WebSocket, client_id: str):
        if len(self.active_connections) >= self.max_connections:
            raise ValueError("Límite de conexiones alcanzado")
            
        await websocket.accept()
        self.active_connections[client_id] = websocket
        logger.info(f"Nueva conexión WebSocket: {client_id}")

    def disconnect(self, client_id: str):
        if client_id in self.active_connections:
            del self.active_connections[client_id]
        if client_id in self.pdf_contents:
            del self.pdf_contents[client_id]
        logger.info(f"Conexión cerrada: {client_id}")

    async def send_message(self, message: str, client_id: str):
        if client_id in self.active_connections:
            try:
                await self.active_connections[client_id].send_text(message)
            except Exception as e:
                logger.error(f"Error enviando mensaje: {e}")
                self.disconnect(client_id)

    def store_pdf_content(self, client_id: str, content: str):
        self.pdf_contents[client_id] = content
        logger.info(f"PDF almacenado para cliente: {client_id}")

    async def process_pdf(self, client_id: str, pdf_data: str):
        try:
            pdf_bytes = base64.b64decode(pdf_data.split(',')[1])
            pdf_file = BytesIO(pdf_bytes)
            
            reader = PdfReader(pdf_file)
            text_content = ""
            for page in reader.pages:
                text_content += page.extract_text() + "\n"
            
            self.store_pdf_content(client_id, text_content)
            return {"status": "success", "message": "PDF procesado correctamente"}
            
        except Exception as e:
            logger.error(f"Error procesando PDF: {e}")
            return {"status": "error", "message": str(e)}