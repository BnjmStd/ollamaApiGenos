import asyncio
import websockets
import json
from datetime import datetime
import aiohttp

async def get_metrics():
    """Obtiene las métricas del servidor"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('http://localhost:8000/metrics') as response:
                if response.status == 200:
                    data = await response.json()
                    metrics = data.get('ollama', {})
                    return {
                        "requests": metrics.get('requests', 0),
                        "errors": metrics.get('errors', 0),
                        "memory": f"{metrics.get('memory_usage', 0) / (1024*1024):.2f} MB",
                        "cpu": f"{metrics.get('cpu_percent', 0):.1f}%"
                    }
                return {"error": f"Status code: {response.status}"}
    except Exception as e:
        return {"error": str(e)}

async def print_metrics():
    """Imprime las métricas actuales"""
    try:
        metrics = await get_metrics()
        print("\n=== Métricas ===")
        if "error" in metrics:
            print(f"Error obteniendo métricas: {metrics['error']}")
        else:
            print(f"Solicitudes totales: {metrics['requests']}")
            print(f"Errores totales: {metrics['errors']}")
            print(f"Uso de memoria: {metrics['memory']}")
            print(f"Uso de CPU: {metrics['cpu']}")
        print("==============\n")
    except Exception as e:
        print(f"Error obteniendo métricas: {e}")

async def test_chat():
    try:
        uri = "ws://localhost:8000/chat/ws/test123"
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Conectando a {uri}...")
        
        async with websockets.connect(uri) as websocket:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ¡Conectado al WebSocket!")
            
            while True:
                # Mostrar métricas antes de la pregunta
                await print_metrics()
                
                question = input("\nEscribe tu pregunta (o 'salir' para terminar): ")
                
                if question.lower() == 'salir':
                    print("\nFinalizando chat...")
                    break
                
                if not question.strip():
                    print("La pregunta no puede estar vacía")
                    continue
                
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Enviando pregunta...")
                message = {
                    "type": "question",
                    "question": question
                }
                
                await websocket.send(json.dumps(message))
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Esperando respuesta...")
                
                response = await websocket.recv()
                response_data = json.loads(response)
                
                if response_data.get("type") == "error":
                    print(f"\n❌ Error: {response_data.get('data', {}).get('message', 'Error desconocido')}")
                else:
                    print(f"\n✅ Respuesta: {response_data.get('data', {}).get('response', '')}")
                
                # Mostrar métricas después de la respuesta
                await print_metrics()
            
    except websockets.exceptions.ConnectionClosed as e:
        print(f"\n❌ La conexión se cerró: {e}")
    except ConnectionRefusedError:
        print(f"\n❌ No se pudo conectar al servidor en {uri}")
    except Exception as e:
        print(f"\n❌ Error inesperado: {type(e).__name__} - {str(e)}")
    finally:
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Sesión finalizada")
        await print_metrics()

if __name__ == "__main__":
    print("=== Test de Chat con Ollama ===")
    try:
        asyncio.get_event_loop().run_until_complete(test_chat())
    except KeyboardInterrupt:
        print("\n\nTest interrumpido por el usuario")
    except Exception as e:
        print(f"\n❌ Error fatal: {type(e).__name__} - {str(e)}")