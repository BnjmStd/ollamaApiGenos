from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
from .manager import ConnectionManager
from .services import OllamaService
import json
from loguru import logger
import asyncio

router = APIRouter()
manager = ConnectionManager()
ollama_service = OllamaService()

@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket, client_id)
    try:
        while True:
            data = await websocket.receive_json()
            logger.info(f"Mensaje recibido de {client_id}")
            
            message_type = data.get("type")
            
            if message_type == "pdf":
                pdf_data = data.get("data")
                result = await manager.process_pdf(client_id, pdf_data)
                await manager.send_message(
                    json.dumps({"type": "pdf_processed", "data": result}),
                    client_id
                )
                
            elif message_type == "question":
                question = data.get("question", "").strip()
                if not question:
                    await manager.send_message(
                        json.dumps({
                            "type": "error",
                            "data": {"message": "La pregunta no puede estar vacía"}
                        }),
                        client_id
                    )
                    continue
                    
                context = manager.pdf_contents.get(client_id)
                response = await ollama_service.get_response(
                    question=question,
                    context=context
                )
                
                await manager.send_message(
                    json.dumps({
                        "type": "response",
                        "data": {"response": response}
                    }),
                    client_id
                )

    except WebSocketDisconnect:
        manager.disconnect(client_id)
    except Exception as e:
        logger.error(f"Error en WebSocket: {e}")
        manager.disconnect(client_id)