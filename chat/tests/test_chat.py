# chat/tests/test_chat.py
import asyncio
import websockets
import json
from loguru import logger

async def test_chat():
    try:
        uri = "ws://localhost:8001/ws/test_client"
        async with websockets.connect(uri) as websocket:
            question = {
                "type": "question",
                "question": "¿Cuáles son los objetivos del tratamiento del cáncer de mama?"
            }
            
            await websocket.send(json.dumps(question))
            response = await websocket.recv()
            print(f"Respuesta del chat:\n{response}")
            
    except Exception as e:
        logger.error(f"Error: {e}")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test_chat())