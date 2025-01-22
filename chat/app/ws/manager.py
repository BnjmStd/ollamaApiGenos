# chat/app/ws/manager.py
from fastapi import WebSocket
from typing import Dict
from loguru import logger

class ConnectionManager:
   def __init__(self):
       # Almacenar conexiones activas
       self.active_connections: Dict[str, WebSocket] = {}
       # Límites de conexión
       self.max_connections = 10000
       self.connection_timeout = 600

   async def connect(self, websocket: WebSocket, client_id: str):
       if len(self.active_connections) >= self.max_connections:
           raise ValueError("Límite de conexiones alcanzado")
       await websocket.accept()
       self.active_connections[client_id] = websocket
       logger.info(f"Nueva conexión: {client_id}")

   def disconnect(self, client_id: str):
       if client_id in self.active_connections:
           del self.active_connections[client_id]
           logger.info(f"Desconexión: {client_id}")

   async def send_message(self, message: str, client_id: str):
       if client_id in self.active_connections:
           try:
               await self.active_connections[client_id].send_text(message)
           except Exception as e:
               logger.error(f"Error enviando mensaje: {e}")
               self.disconnect(client_id)

   async def cleanup(self):
       # Limpiar conexiones al cerrar
       for client_id in list(self.active_connections.keys()):
           self.disconnect(client_id)