from typing import List, Dict, Tuple, Any, Optional
from loguru import logger
import re
from exam_types.exam_patterns import EXAM_PATTERNS
from exam_types.component_aliases import COMPONENT_ALIASES
from exam_types.units_config import COMMON_UNITS
from exam_types.result_patterns import (
    RESULT_PATTERNS,
    REFERENCE_PATTERNS,
    TABLE_FORMATS,
    SKIP_PATTERNS,
    SECTION_BREAKS,
)

class MedicalExamDetector:
    def __init__(self):
        self.medical_indicators = [
            "LABORATORIO", "HOSPITAL", "CLINICA",
            "RESULTADO", "INFORME", "EXAMEN"
        ]

    async def detect_medical_exam(self, text: str) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
        """
        Proceso de detección:
        1. Verifica si es un documento médico
        2. Busca nombres de exámenes en el texto
        3. Para cada examen encontrado, busca sus componentes
        """
        try:
            text = text.upper()
            detected_exams = []
            
            # Paso 1: Verificar si es documento médico
            if not self._is_medical_document(text):
                logger.debug("El documento no parece ser un examen médico")
                return [], {"is_medical": False}
            
            logger.debug("Documento identificado como examen médico")

            # Paso 2: Buscar tipos de examen (Futuramente verificar por nombre completo real y luego coincidencias)
            for exam_name, patterns in EXAM_PATTERNS.items():
                # Buscar coincidencias por nombre
                found_names = []
                for name in patterns['nombres']:
                    if re.search(rf"\b{re.escape(name)}\b", text):
                        found_names.append(name)
                        logger.debug(f"Encontrado examen tipo: {exam_name} ({name})")

                if found_names:
                    # Paso 3: Buscar componentes del examen (Futuramente verificar por nombre completo real y luego coincidencias)
                    found_components = []
                    for component in patterns['componentes']:
                        if self._find_component_in_text(text, component):
                            found_components.append(component)
                            logger.debug(f"Encontrado componente: {component}")
                        elif component in COMPONENT_ALIASES:
                            # Buscar aliases
                            for alias in COMPONENT_ALIASES[component]:
                                if self._find_component_in_text(text, alias):
                                    found_components.append(component)
                                    logger.debug(f"Encontrado componente por alias: {component} ({alias})")
                                    break

                    # Si encontró al menos un componente, agregar el examen
                    if found_components:
                        exam_data = {
                            "name": exam_name,
                            "confidence": 1.0,
                            "patterns": patterns,
                            "found": {
                                "nombres": found_names,
                                "componentes": found_components
                            }
                        }
                        detected_exams.append(exam_data)
                        logger.debug(f"Agregado examen {exam_name} con {len(found_components)} componentes")

            # Logging final
            if detected_exams:
                logger.debug(f"Total exámenes detectados: {len(detected_exams)}")
                for exam in detected_exams:
                    logger.debug(f"Examen: {exam['name']}, Componentes: {exam['found']['componentes']}")
            else:
                logger.debug("No se detectaron exámenes con componentes válidos")

            return detected_exams, {
                "is_medical": True,
                "total_detected": len(detected_exams)
            }

        except Exception as e:
            logger.error(f"Error en detect_medical_exam: {str(e)}", exc_info=True)
            return [], {"error": str(e)}

    def _is_medical_document(self, text: str) -> bool:
        """Verifica si el texto es un documento médico."""
        count = sum(1 for indicator in self.medical_indicators 
                   if indicator in text)
        return count >= 2

    def _find_component_in_text(self, text: str, component: str) -> bool:
        """
        Busca un componente en el texto usando los patrones predefinidos.
        """
        try:
            component_pattern = re.escape(component)
            result_found = False

            # 1. Encontrar el componente en el texto
            component_matches = []
            base_patterns = [
                rf"\b{component_pattern}\b",
                rf"\b{component_pattern}[\s.:](.*?)\b"
            ]

            for pattern in base_patterns:
                matches = re.finditer(pattern, text, re.IGNORECASE)
                component_matches.extend([(m.start(), m.end()) for m in matches])

            # 2. Para cada coincidencia del componente, buscar resultados en el contexto
            for start, end in component_matches:
                # Obtener contexto después del componente
                context = text[end:end + 100]

                # A. Buscar usando RESULT_PATTERNS definidos
                for pattern_type, pattern in RESULT_PATTERNS.items():
                    if re.search(pattern, context):
                        result_found = True
                        logger.debug(f"Componente {component} encontrado con {pattern_type}")
                        break

                if result_found:
                    break

                # B. Buscar usando REFERENCE_PATTERNS definidos
                for ref_type, pattern in REFERENCE_PATTERNS.items():
                    if re.search(pattern, context):
                        result_found = True
                        logger.debug(f"Componente {component} encontrado con referencia {ref_type}")
                        break

                if result_found:
                    break

                # C. Buscar unidades definidas en COMMON_UNITS
                for category, units in COMMON_UNITS.items():
                    for unit in units:
                        if unit in context:
                            result_found = True
                            logger.debug(f"Componente {component} encontrado con unidad {unit}")
                            break
                    if result_found:
                        break

            return result_found

        except Exception as e:
            logger.error(f"Error en _find_component_in_text: {str(e)}")
            return False