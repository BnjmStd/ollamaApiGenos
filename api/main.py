import sys
import os
import json
import tempfile
import multiprocessing
import psutil
import time
import base64
import io
from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks, Body, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware
import uvicorn
from loguru import logger
from typing import Optional, List, Set
from pathlib import Path

from config import get_settings
settings = get_settings()

from middleware.rate_limiter import MemoryRateLimiter
from models.schemas import ExamResponse, PDFContent, SingleExam, ExamRequest
from services.exam_detector import MedicalExamDetector
from services.result_extractor import ResultExtractor
from utils.text_extractors import extract_text_from_pdf, extract_patient_data
from exam_types import (
   EXAM_PATTERNS,
   COMPONENT_ALIASES,
   COMMON_UNITS,
   ANALYSIS_METHODS
)

RESULTS_DIR = Path("results")
TEMP_DIR = Path("temp")
LOG_FILE = "api.log"

class TempFileManager:
   def __init__(self):
       self.temp_files: Set[str] = set()

   def add_file(self, filepath: str):
       self.temp_files.add(filepath)

   async def cleanup(self):
       for filepath in self.temp_files.copy():
           try:
               if os.path.exists(filepath):
                   os.unlink(filepath)
                   self.temp_files.remove(filepath)
           except Exception as e:
               logger.error(f"Error cleaning up {filepath}: {e}")

temp_manager = TempFileManager()

def setup_directories():
   for directory in [settings.RESULTS_DIR, settings.TEMP_DIR]:
       directory.mkdir(parents=True, exist_ok=True)

def setup_logging():
   logger.remove()
   logger.add(
       settings.LOG_FILE,
       format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
       level="DEBUG",
       rotation="500 MB",
       retention="30 days"
   )

app = FastAPI(
   title=settings.API_TITLE,
   description=settings.API_DESCRIPTION,
   version=settings.API_VERSION
)

@app.on_event("startup")
async def startup_event():
   setup_directories()
   setup_logging()
   logger.info("API initialized successfully")

@app.on_event("shutdown")
async def shutdown_event():
   await temp_manager.cleanup()
   logger.info("API shutdown complete")

app.add_middleware(
   CORSMiddleware,
   allow_origins=settings.ALLOWED_ORIGINS,
   allow_credentials=True,
   allow_methods=["*"],
   allow_headers=["*"],
)
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])

medical_detector = MedicalExamDetector()
result_extractor = ResultExtractor()
rate_limiter = MemoryRateLimiter()

@app.get("/")
async def root():
   return {
       "status": "active",
       "message": "Medical Exam Processing API is running",
       "version": "1.0.0"
   }

@app.get("/health")
async def health_check():
   return {
       "status": "healthy",
       "system": {
           "cpu_count": multiprocessing.cpu_count(),
           "memory_available": psutil.virtual_memory().available,
           "temp_files": len(temp_manager.temp_files)
       }
   }

@app.get("/metrics")
async def get_metrics():
   try:
       return {
           "timestamp": time.time(),
           "system": {
               "memory_usage": psutil.Process().memory_info().rss,
               "cpu_usage": psutil.Process().cpu_percent(),
               "temp_files": len(temp_manager.temp_files)
           }
       }
   except Exception as e:
       logger.error(f"Error obteniendo métricas: {e}")
       raise HTTPException(status_code=500, detail=str(e))

def validate_pdf_file(file: UploadFile) -> bool:
   try:
       if not file.filename:
           logger.error("No filename provided")
           raise HTTPException(status_code=400, detail="No filename provided")
           
       if not file.filename.lower().endswith('.pdf'):
           logger.error("File must be a PDF")
           raise HTTPException(status_code=400, detail="El archivo debe ser un PDF")
           
       return True
   except Exception as e:
       logger.error(f"Error validating PDF: {str(e)}")
       raise HTTPException(status_code=400, detail=f"Error validating PDF: {str(e)}")

def find_unit_in_line(line: str) -> Optional[str]:
   for units in COMMON_UNITS.values():
       for unit in units:
           if unit in line.upper():
               return unit
   return None

def find_method_in_line(line: str) -> Optional[str]:
   for methods in ANALYSIS_METHODS.values():
       for method in methods:
           if method in line.upper():
               return method
   return None

def save_exam_response_to_file(response: ExamResponse, patient_data: dict, base_filename: str):
   output_path = settings.RESULTS_DIR / f"{base_filename}_response.json"
   with open(output_path, 'w', encoding='utf-8') as f:
       json.dump({
           "patient_data": patient_data,
           "response": response.dict()
       }, f, indent=2, ensure_ascii=False)
   logger.info(f"Saved complete response to {output_path}")

def save_exam_results_to_file(single_exam: SingleExam, patient_data: dict, base_filename: str):
   output_path = RESULTS_DIR / f"{base_filename}_{single_exam.type}.json"
   with open(output_path, 'w', encoding='utf-8') as f:
       json.dump({
           "patient_data": patient_data,
           "exam": single_exam.dict()
       }, f, indent=2, ensure_ascii=False)
   logger.info(f"Saved results to {output_path}")

async def process_exam_section(exam: dict, section_text: str, patient_data: dict, base_filename: str) -> Optional[SingleExam]:
   try:
       exam_name = exam["name"]
       logger.debug(f"Processing exam section: {exam_name}")

       results = await result_extractor.extract_exam_data(section_text, exam)
       
       if not results:
           logger.warning(f"No results found for exam {exam_name}")
           return None

       single_exam = SingleExam(
           type=exam_name,
           confidence=str(exam.get("confidence", 1.0)),
           metadata={
               "nombres": exam["patterns"]["nombres"],
               "componentes": exam["patterns"]["componentes"],
               "found_components": len(results),
               "total_components": len(exam["patterns"]["componentes"]),
               "detected_names": exam["found"]["nombres"]
           },
           data=results,
           raw_text=section_text
       )

       save_exam_results_to_file(single_exam, patient_data, base_filename)
       logger.debug(f"Processed exam {exam_name} with {len(results)} results")
       
       return single_exam

   except Exception as e:
       logger.error(f"Error processing exam section: {str(e)}", exc_info=True)
       return None

def validate_pdf_content(pdf_data: PDFContent) -> bool:
   try:
       if not pdf_data.content:
           logger.error("No PDF content provided")
           raise HTTPException(status_code=400, detail="No PDF content provided")
           
       try:
           base64.b64decode(pdf_data.content)
       except Exception:
           raise HTTPException(status_code=400, detail="Invalid base64 content")
           
       return True
   except Exception as e:
       logger.error(f"Error validating PDF content: {str(e)}")
       raise HTTPException(status_code=400, detail=f"Error validating PDF content: {str(e)}")

@app.post("/classify-exam/")
async def classify_exam(
   request: Request,
   background_tasks: BackgroundTasks,
   exam_request: ExamRequest = Body(...)
):
   await rate_limiter.check_rate_limit(request)
   temp_file_path = None
   try:
       logger.info(f"Processing JSON request with PDF from IP: {request.client.host}")
       
       validate_pdf_content(exam_request.pdf_data)
       pdf_content = base64.b64decode(exam_request.pdf_data.content)
       
       with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
           temp_file_path = tmp.name
           temp_manager.add_file(temp_file_path)
           tmp.write(pdf_content)
       
       file = UploadFile(
           filename=exam_request.pdf_data.name or "document.pdf",
           file=io.BytesIO(pdf_content)
       )

       text = await extract_text_from_pdf(file)
       if not text:
           raise HTTPException(status_code=400, detail="No se pudo extraer texto del PDF")

       patient_data = extract_patient_data(text)
       patient_data["metadata"].update({
           "original_name": exam_request.pdf_data.name,
           "original_type": exam_request.pdf_data.type,
           "original_date": exam_request.pdf_data.date
       })

       detected_types, metadata = await medical_detector.detect_medical_exam(text)
       logger.debug(f"Detected types: {json.dumps(detected_types, indent=2, ensure_ascii=False)}")
       
       if not detected_types:
           return ExamResponse(
               is_medical=False,
               confidence="0.0",
               metadata=metadata,
               exams=[],
               total_exams=0,
               original_metadata=patient_data["metadata"]
           )

       base_filename = exam_request.pdf_data.name or "document"
       exams = []

       for exam in detected_types:
           single_exam = await process_exam_section(
               exam=exam,
               section_text=text,
               patient_data=patient_data,
               base_filename=base_filename
           )
           if single_exam:
               exams.append(single_exam)

       response = ExamResponse(
           is_medical=True,
           confidence=str(max(exam.get("confidence", 0.0) for exam in detected_types)),
           metadata={
               **metadata,
               "patient_data": patient_data,
               "processed_exams": len(exams)
           },
           exams=exams,
           total_exams=len(exams),
           original_metadata={
               "name": exam_request.pdf_data.name,
               "type": exam_request.pdf_data.type,
               "date": exam_request.pdf_data.date
           }
       )

       return response

   except Exception as e:
       logger.error(f"Error processing exam: {e}", exc_info=True)
       raise HTTPException(status_code=500, detail=str(e))
   finally:
       if temp_file_path:
           background_tasks.add_task(temp_manager.cleanup)

@app.get("/rate-limit-status")
async def get_rate_limit_status(request: Request):
   ip = request.client.host
   current_time = time.time()
   
   requests_last_minute = len([
       req_time for req_time in rate_limiter.requests.get(ip, [])
       if current_time - req_time < 60
   ])
   
   requests_last_hour = len([
       req_time for req_time in rate_limiter.requests.get(ip, [])
       if current_time - req_time < 3600
   ])

   return {
       "ip_info": {
           "ip": ip,
           "requests_last_minute": requests_last_minute,
           "requests_last_hour": requests_last_hour,
           "total_requests": len(rate_limiter.requests.get(ip, [])),
       },
       "system_info": {
           "concurrent_requests": rate_limiter.concurrent_requests,
           "memory_usage_mb": round(psutil.Process().memory_info().rss / (1024 * 1024), 2),
           "memory_percent": round(psutil.Process().memory_percent(), 2),
           "cpu_percent": round(psutil.Process().cpu_percent(), 2),
       },
       "rate_limit_info": {
           "limit_per_minute": settings.RATE_LIMIT_PER_MINUTE,
           "remaining_requests": settings.RATE_LIMIT_PER_MINUTE - requests_last_minute,
           "cleanup_age_seconds": round(current_time - rate_limiter.last_cleanup, 2),
           "total_ips_tracked": len(rate_limiter.requests),
       }
   }
   
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
   logger.error(f"Global exception handler: {exc}", exc_info=True)
   return {"detail": str(exc)}, 500

if __name__ == "__main__":
   logger.info("Starting server...")
   
   config = uvicorn.Config(
       "main:app",
       host=settings.SERVER_HOST,
       port=settings.SERVER_PORT,
       workers=settings.SERVER_WORKERS,
       limit_concurrency=settings.SERVER_LIMIT_CONCURRENCY,
       backlog=settings.SERVER_MAX_REQUESTS,
       log_level="info",
       proxy_headers=True,
       forwarded_allow_ips="*",
       access_log=False
   )
   
   server = uvicorn.Server(config)
   server.run()