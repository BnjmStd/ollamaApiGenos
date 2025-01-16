from typing import List, Dict, Optional, Any
import re
from loguru import logger
from exam_types.exam_patterns import EXAM_PATTERNS
from exam_types.component_aliases import COMPONENT_ALIASES
from exam_types.units_config import COMMON_UNITS
from exam_types.result_patterns import (
    RESULT_PATTERNS,
    REFERENCE_PATTERNS,
    TABLE_FORMATS,
    SKIP_PATTERNS,
    SECTION_BREAKS
)
from exam_types.methods_config import ANALYSIS_METHODS

class ResultExtractor:
    def __init__(self):
        self.result_patterns = RESULT_PATTERNS
        self.reference_patterns = REFERENCE_PATTERNS
        self.common_units = COMMON_UNITS
        self.analysis_methods = ANALYSIS_METHODS

    async def extract_exam_data(self, text: str, exam_type: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extrae datos basándose en los componentes definidos para este tipo de examen.
        """
        try:
            results = []
            lines = text.split('\n')
            
            # Obtener solo los componentes de este tipo de examen
            exam_components = exam_type['patterns']['componentes']
            logger.debug(f"Buscando componentes para {exam_type['name']}: {exam_components}")
            
            # Para cada línea
            for line in lines:
                line_upper = line.upper().strip()
                
                # Para cada componente definido en este tipo de examen
                for component in exam_components:
                    # Si encuentra el componente o uno de sus aliases
                    if self._component_matches(line_upper, component):
                        # Procesar la línea y extraer datos
                        result = self._extract_component_data(line, component)
                        if result:
                            results.append(result)
                            break  
            
            return results
            
        except Exception as e:
            logger.error(f"Error en extract_exam_data: {str(e)}")
            return []

    def _component_matches(self, line: str, component: str) -> bool:
        """
        Verifica si el componente o sus aliases están en la línea.
        """
        # Verificar componente principal
        if re.search(rf"\b{re.escape(component)}\b", line):
            return True
            
        # Verificar aliases si existen
        if component in COMPONENT_ALIASES:
            for alias in COMPONENT_ALIASES[component]:
                if re.search(rf"\b{re.escape(alias)}\b", line):
                    return True
                    
        return False

    def _extract_exact_unit(self, text: str) -> Optional[str]:
        """
        Extrae la unidad y la normaliza al formato estándar definido en COMMON_UNITS.
        """
        # Convertir el texto a una lista de palabras manteniendo los /
        words = text.replace('/',' / ').split()
        
        # Reconstruir posibles unidades del texto
        for i in range(len(words)):
            for j in range(i + 1, len(words) + 1):
                # Reconstruir la unidad potencial
                potential_unit = ''.join(words[i:j]).replace(' ', '')
                
                # Buscar esta unidad en COMMON_UNITS
                for category, units in self.common_units.items():
                    for standard_unit in units:
                        # Comparación insensible a mayúsculas/minúsculas
                        if potential_unit.upper() == standard_unit.upper():
                            # Retornar la unidad en el formato estándar de COMMON_UNITS
                            return standard_unit
        
        return None

    def _find_complete_component_name(self, line: str, component: str) -> str:
        """
        Encuentra el nombre completo del componente de manera flexible.
        Mantiene la flexibilidad pero evita incluir palabras clave del documento.
        """
        line_upper = line.upper()
        common_keywords = [" METODO:", " MÉTODO:", " VALOR:", " RESULTADO:", " MUESTRA:"]
        
        # Lista para almacenar posibles coincidencias
        matches = []
        
        # 1. Buscar componente base y extensiones
        start_idx = line_upper.find(component)
        if start_idx >= 0:
            next_content = line_upper[start_idx:]
            
            # Primero buscar si hay palabras clave que limiten el nombre
            keyword_positions = []
            for keyword in common_keywords:
                key_idx = next_content.find(keyword)
                if key_idx > 0:  # Solo si está después del inicio
                    keyword_positions.append(key_idx)
            
            # Buscar el siguiente número o símbolo
            number_match = re.search(r'\s+\d', next_content)
            punct_match = re.search(r'[,:;]', next_content)
            
            # Determinar dónde termina el nombre del componente
            end_positions = []
            
            if keyword_positions:
                end_positions.append(min(keyword_positions))
            if number_match:
                end_positions.append(number_match.start())
            if punct_match:
                end_positions.append(punct_match.start())
                
            if end_positions:
                # Tomar la posición más cercana
                end_idx = start_idx + min(end_positions)
                matches.append(line_upper[start_idx:end_idx].strip())
            else:
                # Si no hay límites, tomar palabras completas hasta el próximo espacio
                words = next_content.split()
                complete_name = []
                for word in words:
                    if any(keyword.strip(":") in word for keyword in common_keywords):
                        break
                    complete_name.append(word)
                if complete_name:
                    matches.append(' '.join(complete_name))

        # 2. Buscar en aliases (mantener la misma lógica para aliases)
        if component in COMPONENT_ALIASES:
            for alias in COMPONENT_ALIASES[component]:
                start_idx = line_upper.find(alias)
                if start_idx >= 0:
                    next_content = line_upper[start_idx:]
                    # Aplicar la misma lógica que arriba...
                    keyword_positions = []
                    for keyword in common_keywords:
                        key_idx = next_content.find(keyword)
                        if key_idx > 0:
                            keyword_positions.append(key_idx)
                    
                    number_match = re.search(r'\s+\d', next_content)
                    punct_match = re.search(r'[,:;]', next_content)
                    
                    end_positions = []
                    if keyword_positions:
                        end_positions.append(min(keyword_positions))
                    if number_match:
                        end_positions.append(number_match.start())
                    if punct_match:
                        end_positions.append(punct_match.start())
                        
                    if end_positions:
                        end_idx = start_idx + min(end_positions)
                        matches.append(line_upper[start_idx:end_idx].strip())

        # 3. Si no encontramos coincidencias, devolver el componente original
        if not matches:
            return component
            
        # Retornar la coincidencia más larga
        return max(matches, key=len) if matches else component


    def _extract_component_data(self, line: str, component: str) -> Optional[Dict[str, Any]]:
        """
        Extrae información del componente usando los patrones predefinidos.
        """
        try:
            line_upper = line.upper().strip()
            
            # Inicializar el resultado
            result = {
                "componente": "",
                "linea_original": line.strip(),
                "valor": None,
                "tipo_resultado": None,
                "unidad": None,
                "rango_referencia": None,
                "metodo": None
            }

            # 1. Extraer el nombre del componente
            result["componente"] = self._find_complete_component_name(line, component)
            if not result["componente"]:
                return None

            # Remover el nombre del componente
            remaining_text = line_upper.replace(result["componente"], '', 1).strip()

            # 2. Intentar extraer primero resultado cualitativo
            qual_match = re.search(self.result_patterns["qualitative"], remaining_text)
            if qual_match:
                result["valor"] = qual_match.group(1)
                result["tipo_resultado"] = "qualitative"
                remaining_text = remaining_text.replace(qual_match.group(1), '', 1).strip()
            else:
                # 3. Si no es cualitativo, intentar numérico
                num_match = re.search(r'\s*(\d+[.,]?\d*)\s*', remaining_text)
                if num_match:
                    result["valor"] = num_match.group(1).replace(',', '.')
                    result["tipo_resultado"] = "numeric"
                    remaining_text = remaining_text[len(num_match.group(0)):].strip()

                    # Solo buscar unidad si es numérico
                    exact_unit = self._extract_exact_unit(line)
                    if exact_unit:
                        result["unidad"] = exact_unit
                        remaining_text = remaining_text.replace(exact_unit.upper(), '', 1).strip()

            # 4. Extraer rango de referencia
            for ref_type, pattern in self.reference_patterns.items():
                ref_match = re.search(pattern, remaining_text)
                if ref_match:
                    ref_text = ref_match.group(0)
                    numbers = re.findall(r'\d+[.,]?\d*', ref_text)
                    
                    if ref_type == "RANGO" and len(numbers) >= 2:
                        result["rango_referencia"] = {
                            "tipo": "rango",
                            "min": float(numbers[0].replace(',', '.')),
                            "max": float(numbers[1].replace(',', '.'))
                        }
                    elif ref_type in ["HASTA", "MENOR"]:
                        result["rango_referencia"] = {
                            "tipo": "hasta",
                            "max": float(numbers[0].replace(',', '.'))
                        }
                    elif ref_type == "MAYOR":
                        result["rango_referencia"] = {
                            "tipo": "mayor",
                            "min": float(numbers[0].replace(',', '.'))
                        }
                    remaining_text = remaining_text.replace(ref_text, '', 1).strip()
                    break

            # 5. Extraer método
            # Primero buscar después de "METODO:" o "MÉTODO:"
            method_match = re.search(r'(?:METODO|MÉTODO)\s*:\s*(\w+)', remaining_text)
            if method_match:
                method_text = method_match.group(1)
                for category, methods in self.analysis_methods.items():
                    if method_text in methods:
                        result["metodo"] = method_text
                        break
            
            # Si no se encontró después de "METODO:", buscar en el texto restante
            if not result["metodo"]:
                for category, methods in self.analysis_methods.items():
                    for method in methods:
                        if method in remaining_text:
                            result["metodo"] = method
                            break
                    if result["metodo"]:
                        break

            # Validar que tenemos al menos un valor
            if not result["valor"]:
                return None

            return result

        except Exception as e:
            logger.error(f"Error extrayendo datos del componente {component}: {str(e)}")
            return None