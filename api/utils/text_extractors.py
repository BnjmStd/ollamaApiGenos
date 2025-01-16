from loguru import logger
from typing import Optional, Dict, Any, List
from fastapi import UploadFile
import re
from PyPDF2 import PdfReader
from datetime import datetime
from utils.text_normalizer import TextNormalizer  

async def extract_text_from_pdf(file: UploadFile) -> Optional[str]:
    """Extrae texto de un archivo PDF utilizando PyPDF2."""
    try:
        content = await file.read()
        with open("temp.pdf", "wb") as temp_file:
            temp_file.write(content)

        reader = PdfReader("temp.pdf")
        full_text = []
        for page in reader.pages:
            text = page.extract_text()
            if text:
                full_text.append(text)

        extracted_text = "\n".join(full_text)

        if not extracted_text.strip():
            logger.warning("El PDF no contiene texto extraíble.")
            return None

        logger.info("Texto extraído del PDF exitosamente.")
        return extracted_text
    except Exception as e:
        logger.error(f"Error al extraer texto del PDF: {e}")
        return None


def extract_patient_data(text: str) -> Dict[str, Any]:
    """Extrae datos personales del texto del PDF."""
    try:
        patient_data = {}
        lines = text.split('\n')

        # Debug: Mostrar todo el texto para identificar problemas
        logger.debug("Texto completo a procesar:")
        logger.debug(text)

        # Buscar RUT: Adaptar patrón según formato del país
        rut_pattern = r'\b(\d{7,8}-[\dkK])\b'
        rut_match = re.search(rut_pattern, text)
        if rut_match:
            patient_data['rut'] = rut_match.group(1)
            logger.debug(f"RUT encontrado: {patient_data['rut']}")
        else:
            logger.warning("No se encontró RUT en el texto.")

        # Buscar Nombre del Paciente
        found_name = False
        for line in lines:
            if 'NOMBRE' in line.upper() or 'PACIENTE' in line.upper():
                if ':' in line:
                    name = line.split(':', 1)[1].strip()
                    if name and not any(x in name.upper() for x in ['OBSERVACION', 'NO INDICADO']):
                        patient_data['nombre'] = TextNormalizer.normalize_name(name)
                        logger.debug(f"Nombre encontrado: {patient_data['nombre']}")
                        found_name = True
                        break
        if not found_name:
            logger.warning("No se encontró el nombre del paciente.")

        # Buscar Edad
        age_pattern = r'\bEdad[:\s]+(\d{1,3})\b'
        age_match = re.search(age_pattern, text, re.IGNORECASE)
        if age_match:
            patient_data['edad'] = age_match.group(1)
            logger.debug(f"Edad encontrada: {patient_data['edad']}")
        else:
            logger.warning("No se encontró la edad del paciente.")

        # Agregar Metadata
        patient_data["metadata"] = {
            "fecha_procesamiento": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "tipo_documento": "Examen Clínico",
            "campos_encontrados": list(k for k in patient_data.keys() if k != "metadata"),
        }

        logger.debug(f"Datos extraídos finales: {patient_data}")
        return patient_data

    except Exception as e:
        logger.error(f"Error en extract_patient_data: {e}")
        return {
            "metadata": {
                "fecha_procesamiento": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "tipo_documento": "Examen Clínico",
                "error": str(e),
            }
        }


def extract_exam_results(text: str, components: List[str]) -> Dict[str, Any]:
    """Extrae resultados de exámenes del texto."""
    results = {}

    for component in components:
        # Patrón para buscar el componente y su valor asociado
        pattern = rf"{re.escape(component)}[:\s]+([^:\n]+)"
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            value = match.group(1).strip()
            # Normalizar solo si parece un valor numérico
            if re.match(r'^[\d.,]+$', value):
                results[component] = TextNormalizer.normalize_value(value)
            else:
                results[component] = value

    if not results:
        logger.warning("No se encontraron resultados de exámenes en el texto.")
    else:
        logger.info(f"Resultados extraídos: {results}")

    return results
