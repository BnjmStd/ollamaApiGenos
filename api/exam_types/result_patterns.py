# Patrones para resultados con mayor flexibilidad
RESULT_PATTERNS = {
    "numeric": r"(\d+[.,]?\d*)\s*(?:[A-Z/%]+(?:[/\s]*[A-Z0-9^]+)*)",
    "qualitative": r"((?:NO\s+)?(?:REACTIVO|POSITIVO|NEGATIVO|NORMAL|ANORMAL|BAJO|ALTO|ELEVADO|DISMINUIDO))",
    "ratio": r"(\d+[.,]?\d*)\s*(?:INDICE|RATIO|RELACION|INDEX)",
    "range": r"(\d+[.,]?\d*)\s*[-–]\s*(\d+[.,]?\d*)",
    "time": r"(\d+[.,]?\d*)\s*(?:SEG|MIN|HRS?|SEGUNDOS?|MINUTOS?|HORAS?)",
    "cell_count": r"(\d+[.,]?\d*)\s*(?:X\s*10\^[36]|[/\\][UuµMm][Ll]|MM3)"
}

# Patrones para rangos de referencia
REFERENCE_PATTERNS = {
    "RANGO": r"\d+[.,]?\d*\s*[-–]\s*\d+[.,]?\d*",
    "HASTA": r"(?:HASTA|MENOR\s+(?:A|DE|QUE)?|<|MAXIMO)\s*\d+[.,]?\d*",
    "MENOR": r"[<>≤≥]\s*\d+[.,]?\d*",
    "MAYOR": r"(?:MAYOR|SUPERIOR|>)\s*(?:A|DE|QUE)?\s*\d+[.,]?\d*",
    "NORMAL": r"(?:NORMAL|NEGATIVO|POSITIVO|NO\s+REACTIVO|REACTIVO)"
}

# Formatos de tabla
TABLE_FORMATS = {
    "simple": r"\s{2,}|\t",      
    "lined": r"\|",              
    "csv": r",|;",               
    "mixed": r"[\t|,;]|\s{2,}"   
}

# Patrones para saltar líneas
SKIP_PATTERNS = [
    "PARÁMETRO", "FECHA[: ]", "TECNOLOGÍA[: ]", "INFORME",
    "PACIENTE", "EDAD", "RUT", "SOLICITANTE",
    "RESULTADO", "MUESTRA", "MÉTODO", "OBSERVACIONES?"
]

# Patrones para detectar fin de sección
SECTION_BREAKS = [
    r"^[-=_*]{3,}$",            # Líneas de separación
    r"^\s*$",                   # Líneas vacías
    r"^[A-Z\s]{10,}:?$",        # Títulos en mayúsculas
    r"^(?:RESULTADOS?|INFORME|OBSERVACIONES?):"  # Palabras clave
]