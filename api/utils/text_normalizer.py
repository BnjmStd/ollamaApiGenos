from typing import Dict, Tuple, Optional, List, Any
import re
from loguru import logger

class TextNormalizer:
    @staticmethod
    def normalize_text(text: str) -> str:
        """
        Normaliza el texto completo para procesamiento.
        """
        try:
            # Eliminar caracteres especiales excepto los importantes
            text = re.sub(r'[^\w\s,.;:()/\-+]', ' ', text)
            # Normalizar espacios
            text = ' '.join(text.split())
            # Convertir a mayúsculas
            return text.upper()
        except Exception as e:
            logger.error(f"Error normalizing text: {str(e)}")
            return text

    @staticmethod
    def normalize_value(value: str) -> str:
        """
        Normaliza valores numéricos con mejor manejo de formatos.
        """
        try:
            # Eliminar espacios
            value = value.strip().replace(' ', '')
            # Reemplazar comas por puntos
            value = value.replace(',', '.')
            
            # Manejar múltiples puntos decimales
            if value.count('.') > 1:
                parts = value.split('.')
                value = ''.join(parts[:-1]) + '.' + parts[-1]
            
            # Validar formato numérico
            if not re.match(r'^\d*\.?\d+$', value):
                return ""
                
            return value
            
        except Exception as e:
            logger.error(f"Error normalizing value: {str(e)}")
            return ""

    @staticmethod
    def normalize_unit(unit: str) -> str:
        """
        Mantiene las unidades exactamente como aparecen en el texto original.
        Ya no normaliza, solo valida que la unidad existe en COMMON_UNITS.
        """
        if not unit:
            return ""
            
        unit = unit.strip().upper()
        
        # Buscar la unidad en todas las categorías
        for category_units in COMMON_UNITS.values():
            if unit in category_units:
                return unit  # Retorna la unidad exactamente como viene
                
        return unit  # Si no encuentra la unidad, la retorna igual

    @staticmethod
    def normalize_method(method: str) -> str:
        """
        Mantiene los métodos exactamente como aparecen en el texto original.
        Solo valida que el método existe en ANALYSIS_METHODS.
        """
        if not method:
            return ""
            
        method = method.strip().upper()
        
        # Buscar el método en todas las categorías
        for category_methods in ANALYSIS_METHODS.values():
            for m in category_methods:
                # Permitir variaciones con guiones y espacios
                pattern = m.replace('-', '[-\\s]*')
                if re.match(pattern, method):
                    return method  # Retorna el método exactamente como viene
                    
        return method  # Si no encuentra el método, lo retorna igual

    @staticmethod
    def normalize_reference_range(text: str) -> Dict[str, Optional[float]]:
        """
        Extrae y normaliza rangos de referencia con más formatos.
        """
        if not text:
            return {}
        
        try:
            text = text.upper()
            result = {}
            
            # Patrones de rango expandidos
            patterns = [
                # Rango numérico (X - Y)
                r'(\d+\.?\d*)\s*[-–]\s*(\d+\.?\d*)',
                # Hasta X
                r'HASTA\s*(\d+\.?\d*)',
                # Mayor/Menor que
                r'(?:>|MAYOR\s*(?:A|DE|QUE)?\s*)(\d+\.?\d*)',
                r'(?:<|MENOR\s*(?:A|DE|QUE)?\s*)(\d+\.?\d*)',
                # Entre X y Y
                r'ENTRE\s*(\d+\.?\d*)\s*Y\s*(\d+\.?\d*)'
            ]
            
            for pattern in patterns:
                match = re.search(pattern, text)
                if match:
                    if len(match.groups()) == 2:
                        result['min_value'] = float(match.group(1))
                        result['max_value'] = float(match.group(2))
                    elif 'HASTA' in text or '<' in text or 'MENOR' in text:
                        result['max_value'] = float(match.group(1))
                    else:
                        result['min_value'] = float(match.group(1))
                    break
            
            return result
            
        except Exception as e:
            logger.error(f"Error normalizing reference range: {str(e)}")
            return {}

    @staticmethod
    def clean_component_name(name: str) -> str:
        """
        Limpia y normaliza nombres de componentes.
        """
        try:
            # Eliminar caracteres especiales
            name = re.sub(r'[^\w\s/-]', '', name)
            # Normalizar espacios
            name = ' '.join(name.split())
            return name.upper()
        except Exception as e:
            logger.error(f"Error cleaning component name: {str(e)}")
            return name

    @staticmethod
    def normalize_name(text: str, field_type: str = None) -> str:
        """
        Normaliza nombres de pacientes con diferentes formatos.
        
        Args:
            text (str): Texto a normalizar
            field_type (str): Tipo de campo (nombre, paciente, etc.)
        """
        try:
            # Limpiar el texto
            text = text.strip()
            
            # Identificar el formato
            if ',' in text:  # Formato: "APELLIDOS, NOMBRES"
                parts = text.split(',')
                text = f"{parts[1].strip()} {parts[0].strip()}"
            elif ':' in text:  # Formato: "PACIENTE: NOMBRES APELLIDOS"
                text = text.split(':', 1)[1].strip()
                
            # Capitalizar cada palabra
            text = ' '.join(word.capitalize() for word in text.split())
            
            # Eliminar palabras clave comunes
            words_to_remove = [
                'paciente', 'nombre', 'edad', 'rut', 'dni', 
                'señor', 'señora', 'sr', 'sra', 'don', 'doña'
            ]
            pattern = r'\b(' + '|'.join(words_to_remove) + r')\b'
            text = re.sub(pattern, '', text, flags=re.IGNORECASE)
            
            # Limpiar espacios múltiples
            text = ' '.join(text.split())
            
            return text.strip()
            
        except Exception as e:
            logger.error(f"Error normalizing name: {str(e)}")
            return text

    @staticmethod
    def identify_name_field(text: str) -> Optional[str]:
        """
        Identifica el campo que contiene el nombre del paciente.
        
        Args:
            text (str): Línea de texto a analizar
        Returns:
            Optional[str]: El nombre encontrado o None
        """
        try:
            # Patrones para identificar campos de nombre
            patterns = [
                r"(?:Nombre|Paciente|Nombre del Paciente)\s*:?\s*([A-ZÁ-ÚÑ][A-ZÁ-ÚÑa-záéíóúñ\s,]+)",
                r"(?:Sr\.|Sra\.|Don|Doña)\s+([A-ZÁ-ÚÑ][A-ZÁ-ÚÑa-záéíóúñ\s,]+)",
                r"(?:Patient|Name)\s*:?\s*([A-ZÁ-ÚÑ][A-ZÁ-ÚÑa-záéíóúñ\s,]+)",
                r"^([A-ZÁ-ÚÑ][A-ZÁ-ÚÑa-záéíóúñ\s,]+)(?=\s*\d|\s*,|\s*Edad|\s*RUT)"
            ]
            
            for pattern in patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    return match.group(1)
                    
            return None
            
        except Exception as e:
            logger.error(f"Error identifying name field: {str(e)}")
            return None

    @staticmethod
    def normalize_rut(rut: str) -> str:
        """
        Normaliza RUT/DNI.
        """
        try:
            # Eliminar puntos y espacios
            rut = rut.replace(".", "").replace(" ", "")
            
            # Si no tiene guión y tiene largo correcto
            if "-" not in rut and len(rut) > 1:
                rut = f"{rut[:-1]}-{rut[-1]}"
                
            return rut
        except Exception as e:
            logger.error(f"Error normalizing RUT: {str(e)}")
            return rut

    @staticmethod
    def normalize_age(age_text: str) -> Dict[str, Any]:
        """
        Normaliza texto de edad a componentes estructurados.
        Maneja múltiples formatos flexiblemente:
        """
        try:
            result = {
                "años": 0,
                "meses": 0,
                "dias": 0,
                "edad_completa": ""
            }

            if not age_text:
                return result

            # Limpieza y normalización inicial
            text = age_text.upper().strip()
            logger.debug(f"Procesando edad: {text}")

            # Lista de patrones por prioridad
            patterns = [
                
                (r"(\d+)\s*A\s*(\d+)?\s*M?\s*(\d+)?\s*S?", 1.0),
                
                
                (r"(\d+)\s*(?:AÑOS?|YEAR|Y|A)?\s*(?:(\d+)\s*(?:MESES?|MONTH|M))?\s*(?:(\d+)\s*(?:DIAS?|DAYS?|D|S))?", 0.9),
                
                
                (r"(\d+)\s*(?:AÑOS?|YEAR|Y|A)?", 0.8),
                
                # Solo el número si nada más funciona
                (r"(\d+)", 0.7)
            ]

            best_match = None
            best_confidence = 0

            for pattern, confidence in patterns:
                match = re.search(pattern, text, re.IGNORECASE | re.VERBOSE)
                if match:
                    groups = match.groups()
                    if any(groups):  # Al menos un grupo capturado
                        best_match = match
                        best_confidence = confidence
                        break

            if best_match:
                logger.debug(f"Patrón encontrado con confianza {best_confidence}")
                
                # Extraer valores, usar 0 si no existe el grupo
                years = int(best_match.group(1)) if best_match.group(1) else 0
                months = int(best_match.group(2)) if len(best_match.groups()) > 1 and best_match.group(2) else 0
                days = int(best_match.group(3)) if len(best_match.groups()) > 2 and best_match.group(3) else 0

                result.update({
                    "años": years,
                    "meses": months,
                    "dias": days
                })

                # Construir edad completa
                parts = []
                if years > 0:
                    parts.append(f"{years}a")
                if months > 0:
                    parts.append(f"{months}m")
                if days > 0:
                    parts.append(f"{days}d")

                result["edad_completa"] = " ".join(parts) or "0a"

                # Validación adicional
                if years == 0 and months == 0 and days == 0:
                    logger.warning(f"Se encontró el patrón pero todos los valores son 0: {text}")
                else:
                    logger.debug(f"Edad extraída exitosamente: {result}")

            else:
                logger.warning(f"No se pudo extraer la edad del texto: {text}")

            return result

        except Exception as e:
            logger.error(f"Error normalizando edad: {str(e)}")
            return {
                "años": 0,
                "meses": 0,
                "dias": 0,
                "edad_completa": "0a"
            }