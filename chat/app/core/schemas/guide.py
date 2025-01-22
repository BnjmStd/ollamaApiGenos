from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field

class GuideSection(BaseModel):
    id: str
    titulo: str
    contenido: str
    palabras_clave: List[str]
    subsecciones: List['GuideSection'] = []

class ClinicalGuide(BaseModel):
    id: str
    nombre: str
    descripcion: str
    temas_clave: List[str]
    ultima_actualizacion: str
    secciones: List[GuideSection]