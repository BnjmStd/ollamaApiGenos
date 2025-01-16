from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field

# Clase para el contenido del PDF en el JSON
class PDFContent(BaseModel):
    name: Optional[str] = Field(default=None, description="Nombre del documento")
    type: Optional[str] = Field(default=None, description="Tipo de documento")
    date: Optional[str] = Field(default=None, description="Fecha del documento")
    content: str = Field(..., description="Contenido del PDF en base64")

# Clase para la petición
class ExamRequest(BaseModel):
    pdf_data: PDFContent

# Clase de exámen
class SingleExam(BaseModel):
    type: str
    confidence: str = Field(default="1.0")
    metadata: Dict = Field(default_factory=dict)
    data: List[Dict[str, Any]] = Field(default_factory=list)
    raw_text: Optional[str] = None

class ExamResponse(BaseModel):
    is_medical: bool = Field(default=False)
    confidence: str = Field(default="0.0")
    metadata: Dict = Field(default_factory=dict)
    exams: List[SingleExam] = Field(default_factory=list)
    total_exams: int = Field(default=0)
    json_file: Optional[List[str]] = None
    # Campo para mantener la información original del JSON
    original_metadata: Optional[Dict] = Field(default=None, description="Metadata original del JSON")