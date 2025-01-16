ANALYSIS_METHODS = {
    "GENERAL": [
        "COLORIMETRICO", "ESPECTROFOTOMETRICO", 
        "TURBIDIMETRICO", "NEFELOMETRICO",
        # Variantes con espacios y guiones
        "COLOR.", "ESPECT.", "TURB.", "NEF."
    ],
    "BIOQUIMICA": [
        # Métodos enzimáticos
        "CHOD-PAP", "CHOD - PAP", "CHOD PAP",
        "GPO-PAP", "GPO - PAP", "GPO PAP",
        "IFCC", "DSA", "ELISA", "UV-VISIBLE",
        # Otros métodos bioquímicos
        "DIRECTO", "INDIRECTO", "CALCULADO",
        "ENZIMATICO", "CINETICO", "COLORIMETRICO", "ELFA"
    ],
    "HORMONAS": [
        "QUIMIOLUMINISCENCIA", "INMUNOFLUORESCENCIA",
        "ELECTROQUIMICO", "ELECTROQUIMIOLUMINISCENCIA",
        # Variantes abreviadas
        "QUIMIO.", "INMUNO.", "ELECTRO."
    ],
    "MICROBIOLOGIA": [
        "PCR", "CULTIVO", "ELISA", "INMUNOLOGICO",
        "MICROSCOPIA", "TINCION", "GRAM"
    ],
    "SEROLOGIA": [
        "ELISA", "WESTERN BLOT", "INMUNOENZIMATICO",
        "FLUORESCENCIA", "FLUORESCENCIA INDIRECTA",
        # Variantes con guiones
        "WESTERN-BLOT", "INMUNO-ENZIMATICO"
    ],
    "OTROS": [
        "MANUAL", "AUTOMATIZADO", "CALCULADO",
        "UV", "VISIBLE", "IR", "ESPECTROMETRIA"
    ]
}
# Variantes auxiliares (falta implementar más)
METHOD_PARAMETERS = {
    "TEMPERATURA": [
        "37C", "30C", "25C",
        # Variantes con espacios
        "37 C", "30 C", "25 C",
        # Variantes con grados
        "37°C", "30°C", "25°C"
    ],
    "LONGITUD_ONDA": [
        "340nm", "405nm", "505nm", "546nm",
        # Variantes con espacios
        "340 nm", "405 nm", "505 nm", "546 nm"
    ],
    "TIPOS_MUESTRA": [
        "SUERO", "PLASMA", "ORINA", "LCR", 
        "SANGRE TOTAL", "SANGRE VENOSA", "SANGRE ARTERIAL",
        # Abreviaciones comunes
        "S", "P", "O", "ST"
    ],
    "DILUCION": [
        "1:2", "1:4", "1:8", "1:10", "1:20",
        # Variantes con espacios
        "1 : 2", "1 : 4", "1 : 8", "1 : 10"
    ]
}