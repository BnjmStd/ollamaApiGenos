# chat/app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from loguru import logger
from pathlib import Path

from core.config import get_settings
from ws.router import router as ws_router
from services.guide_service import GuideService

settings = get_settings()

app = FastAPI(
   title="Chat Service",
   description="WebSocket service for clinical guides chat"
)

# CORS
app.add_middleware(
   CORSMiddleware,
   allow_origins=["*"],
   allow_credentials=True,
   allow_methods=["*"],
   allow_headers=["*"],
)

# Rutas WebSocket
app.include_router(ws_router)

@app.on_event("startup")
async def startup_event():
   # Inicializar servicios
   Path("guides").mkdir(exist_ok=True)
   logger.info("Chat service initialized")

@app.on_event("shutdown")
async def shutdown_event():
   logger.info("Chat service shutdown complete")

if __name__ == "__main__":
   uvicorn.run(
       "main:app",
       host=settings.CHAT_HOST,
       port=settings.CHAT_PORT,
       workers=settings.CHAT_WORKERS
   )