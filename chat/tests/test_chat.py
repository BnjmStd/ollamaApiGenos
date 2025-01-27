import asyncio
import websockets
import json
from loguru import logger
import time

async def test_chat(questions):
    try:
        uri = "ws://localhost:8001/ws/test_client"
        async with websockets.connect(uri) as websocket:
            for q in questions:
                start_time = time.time()
                
                question = {
                    "type": "question",
                    "question": q
                }
                
                print(f"\nEnviando pregunta: {q}")
                await websocket.send(json.dumps(question))
                response = await websocket.recv()
                
                end_time = time.time()
                print(f"Tiempo de respuesta: {end_time - start_time:.2f} segundos")
                print(f"Respuesta:\n{response}\n")
                print("-" * 80)
                
                # Esperar entre preguntas
                await asyncio.sleep(2)
            
    except Exception as e:
        logger.error(f"Error: {e}")

if __name__ == "__main__":
    test_questions = [
        "¿Cuáles son los objetivos del tratamiento del cáncer de mama?",
        "¿Cuáles son los factores de riesgo del cáncer de próstata?",
        "¿Cómo se realiza el diagnóstico del cáncer vesical?"
    ]
    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test_chat(test_questions))