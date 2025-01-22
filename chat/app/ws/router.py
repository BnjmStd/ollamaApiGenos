# chat/app/ws/router.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from services.query_service import QueryService
from ws.manager import ConnectionManager
import json
from loguru import logger

router = APIRouter()
manager = ConnectionManager()
query_service = QueryService()

@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket, client_id)
    try:
        while True:
            data = await websocket.receive_json()
            if data.get("type") == "question":
                question = data.get("question", "").strip()
                
                if not question:
                    await manager.send_message("Por favor, ingresa una pregunta válida.", client_id)
                    continue

                response = await query_service.process_query(question)
                
                # Enviar solo la respuesta formateada
                await manager.send_message(
                    response['response'],  # Solo se envía el texto de la respuesta
                    client_id
                )

    except WebSocketDisconnect:
        manager.disconnect(client_id)

    except Exception as e:
        logger.error(f"Error en WebSocket: {e}")
        manager.disconnect(client_id)