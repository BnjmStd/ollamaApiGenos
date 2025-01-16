import subprocess
import asyncio
import websockets
import json
import time

async def test_pdf_chat():
    try:
        # 1. Primero enviamos el PDF con curl
        pdf_path = "/home/bastudillo/ollama-chat/api/test_files/cuento.pdf"  # Ruta absoluta
        curl_command = [
            'curl',
            '-X', 'POST',
            'http://localhost:8000/chat/ws/test123',
            '-H', 'Connection: Upgrade',
            '-H', 'Upgrade: websocket',
            '-H', 'Sec-WebSocket-Key: test123',
            '-H', 'Sec-WebSocket-Version: 13',
            '-F', f'file=@{pdf_path}'
        ]
        
        print("Enviando PDF...")
        result = subprocess.run(curl_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Decodificar resultados manualmente para versiones anteriores a Python 3.7
        stdout = result.stdout.decode('utf-8') if result.stdout else ""
        stderr = result.stderr.decode('utf-8') if result.stderr else ""
        
        # Mostrar resultados
        if stdout:
            print(f"Resultado del envío del PDF (stdout): {stdout}")
        if stderr:
            print(f"Error al enviar el PDF (stderr): {stderr}")
        
        time.sleep(2)  # Esperar a que se procese el PDF
        
        # 2. Conectar al WebSocket y hacer preguntas sobre el PDF
        uri = "ws://localhost:8000/chat/ws/test123"
        async with websockets.connect(uri) as websocket:
            print("Conectado al WebSocket!")
            
            # Preguntas predefinidas sobre el PDF
            questions = [
                "¿Cuál es el tema principal de este PDF?",
                "¿Puedes resumir los puntos principales?",
                "¿Qué conclusiones importantes hay?"
            ]
            
            for question in questions:
                print(f"\nEnviando pregunta: {question}")
                await websocket.send(json.dumps({
                    "type": "question",
                    "question": question
                }))
                
                response = await websocket.recv()
                print("\nRespuesta del bot:", json.loads(response))
                time.sleep(1)  # Esperar entre preguntas
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("Iniciando prueba de chat con PDF...")
    asyncio.get_event_loop().run_until_complete(test_pdf_chat())
