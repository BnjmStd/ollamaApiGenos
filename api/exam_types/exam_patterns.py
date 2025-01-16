EXAM_PATTERNS = {
    "HEMOGRAMA": {
        "nombres": [
            "HEMOGRAMA", "HEMOGRAMA COMPLETO", "HEMATOLOGIA", "CBC",
            "CUADRO HEMATICO", "BIOMETRIA HEMATICA", "CITOMETRIA HEMATICA",
            "HEMOGRAMA AUTOMATIZADO"
        ],
        "componentes": [
            "HEMATOCRITO", "HEMOGLOBINA", "GLOBULOS ROJOS", "ERITROCITOS",
            "GLOBULOS BLANCOS", "LEUCOCITOS", "PLAQUETAS", "VCM", "HCM", "CHCM", 
            "VHS", "SEGMENTADOS", "LINFOCITOS", "MONOCITOS", "EOSINOFILOS", 
            "BASOFILOS", "RETICULOCITOS", "RDW", "NEUTROFILOS", "MIELOCITOS",
            "HEMATIES", "SERIE ROJA", "SERIE BLANCA", "FORMULA LEUCOCITARIA"
        ]
    },
    
    "HEPATITIS": {
        "nombres": [
            "HEPATITIS", "VIRUS HEPATITIS", "MARCADORES HEPATITIS",
            "PERFIL HEPATITIS", "SEROLOGIA HEPATITIS", "ANTIGENOS HEPATITIS",
            "PANEL HEPATITIS", "SCREENING HEPATITIS", "MICROBIOLOGIA"
        ],
        "componentes": [
            "HEPATITIS A", "ANTI-HAV", "HAV IGM", "HAV IGG",
            "HEPATITIS B", "HBSAG", "ANTI-HBS", "ANTI-HBC", "HBV DNA",
            "HEPATITIS C", "ANTI-HCV", "HCV", "HCV RNA",
            "HEPATITIS D", "ANTI-HDV", "HDV",
            "HEPATITIS E", "ANTI-HEV", "HEV"
        ]
    },

    "PERFIL_LIPIDICO": {
        "nombres": [
            "PERFIL LIPIDICO", "LIPIDOS", "LIPIDOGRAMA", "PERFIL DE LIPIDOS",
            "PANEL DE LIPIDOS", "COLESTEROL Y TRIGLICERIDOS", "ESTUDIO LIPIDICO",
            "PERFIL LIPIDICO COMPLETO"
        ],
        "componentes": [
            # Colesterol y variantes
            "COLESTEROL TOTAL", "COL TOTAL", "COLESTEROL", "COL-T",
            
            # HDL y variantes
            "COLESTEROL HDL", "HDL", "COL HDL", "HDL-COLESTEROL", "C-HDL",
            "COL-HDL", "COL. HDL", "HDL COLESTEROL", "HDL DIRECTO",
            
            # LDL y variantes
            "COLESTEROL LDL", "LDL", "COL LDL", "LDL-COLESTEROL", "C-LDL",
            "COL-LDL", "COL. LDL", "LDL COLESTEROL", "LDL CALCULADO",
            
            # VLDL y variantes
            "COLESTEROL VLDL", "VLDL", "COL VLDL", "VLDL-COLESTEROL",
            
            # Triglicéridos y variantes
            "TRIGLICERIDOS", "TG", "TRIGLIC", "TRIGLICERIDOS TOTALES", 
            "TRIGLICÉRIDOS", "TAG",
            
            # Índices
            "INDICE (COL. TOTAL/HDL)", "COL-T/HDL", "INDICE ATEROGENICO",
            "RELACION COL/HDL", "INDICE DE CASTELLI", "RELACION LDL/HDL",
            "INDICE COL/HDL", "LDL/HDL", "COL TOTAL/HDL", "INDICE (COL. TOTAL/HDL"
        ]
    },

    "PERFIL_HEPATICO": {
        "nombres": [
            "PERFIL HEPATICO", "PERFIL HEPÁTICO", "PRUEBAS HEPATICAS", "FUNCION HEPATICA", "PFH",
            "ENZIMAS HEPATICAS", "PANEL HEPATICO", "HEPATOGRAMA",
            "TEST HEPATICO", "ESTUDIO HEPATICO", "PRUEBAS DE FUNCION HEPATICA"
        ],
        "componentes": [
            "BILIRRUBINA TOTAL", "BILIRRUBINA DIRECTA", "BILIRRUBINA INDIRECTA",
            "FOSFATASA ALCALINA", "TRANSAMINASA GPT", "TRANSAMINASA GOT",
            "GGT", "GAMMA GT", "GAMMA GLUTAMIL TRANSFERASA",
            "TGO", "TGP", "AST", "ALT", "SGOT", "SGPT",
            "PROTEINAS TOTALES", "ALBUMINA", "GLOBULINA",
            "TIEMPO DE PROTROMBINA", "TIEMPO DE PROTOMBINA", "TP",
            "RELACION ALBUMINA/GLOBULINA", "DHL", "DESHIDROGENASA LACTICA",
            "GPT/ALT", "GOT/AST",
            "TRANSAMINASA GPT/ALT", "TRANSAMINASA GOT/AST",
            "ALANINA AMINOTRANSFERASA", "ASPARTATO AMINOTRANSFERASA",
            "TIEMPO DE PROTROMBINA", "TP", "PROTROMBINA"
        ]
    },

    "PERFIL_TIROIDEO": {
        "nombres": [
            "PERFIL TIROIDEO", "HORMONAS TIROIDEAS", "TIROIDEO",
            "FUNCION TIROIDEA", "PRUEBAS TIROIDEAS", "TIROIDES",
            "PANEL TIROIDEO", "ESTUDIO TIROIDEO"
        ],
        "componentes": [
            "TSH", "T3", "T4", "T3 LIBRE", "T4 LIBRE", "FT3", "FT4",
            "ANTICUERPOS ANTITIROIDEOS", "TIROGLOBULINA", "CALCITONINA",
            "ANTI TPO", "ANTI TG", "TRAB", "ANTICUERPOS ANTI RECEPTOR TSH",
            "ANTICUERPOS ANTIMICROSOMALES", "CAPTACION T3"
        ]
    },

    "PERFIL_BIOQUIMICO": {
        "nombres": [
            "PERFIL BIOQUIMICO", "QUIMICA", "BIOQUIMICA", "QUIMICA SANGUINEA",
            "PERFIL QUIMICO", "PANEL METABOLICO", "BIOQUIMICA COMPLETA",
            "QUIMICA CLINICA", "PERFIL BIOQUIMICO GENERAL"
        ],
        "componentes": [
            "GLICEMIA", "GLUCOSA", "UREA", "CREATININA", "ACIDO URICO",
            "PROTEINAS TOTALES", "ALBUMINA", "GLOBULINA", "CALCIO", "FOSFORO",
            "MAGNESIO", "SODIO", "POTASIO", "CLORO", "BICARBONATO",
            "LDH", "CPK", "AMILASA", "LIPASA", "NITROGENO UREICO",
            "BUN", "ELECTROLITOS", "DESHIDROGENASA LACTICA", "CK", "CK-MB",
            "PROTEINA C REACTIVA", "PCR", "VSG", "VHS"
        ]
    },

    "HORMONAS": {
        "nombres": [
            "HORMONAS", "ESTUDIO HORMONAL", "PANEL HORMONAL",
            "PERFIL HORMONAL", "TEST HORMONALES"
        ],
        "componentes": [
            "CORTISOL", "PROLACTINA", "INSULINA", "TESTOSTERONA", "ESTRADIOL",
            "PROGESTERONA", "FSH", "LH", "HCG", "DHEA", "PTH", "ACTH",
            "HORMONA CRECIMIENTO", "GH", "IGF-1", "SOMATOMEDINA",
            "17 HIDROXIPROGESTERONA", "ANDROSTENEDIONA", "ALDOSTERONA",
            "HORMONA ANTIMULLERIANA", "AMH", "MELATONINA"
        ]
    },

    "FERTILIDAD": {
        "nombres": [
            "FERTILIDAD", "ESTUDIO FERTILIDAD", "PERFIL REPRODUCTIVO",
            "PERFIL GINECOLOGICO", "PERFIL ANDROLOGIA"
        ],
        "componentes": [
            "FSH", "LH", "ESTRADIOL", "PROGESTERONA", "TESTOSTERONA",
            "PROLACTINA", "AMH", "INHIBINA B", "ESPERMOGRAMA",
            "FRUCTOSA SEMINAL", "TEST POST COITAL", "FRAGMENTACION DNA ESPERMATICO"
        ]
    },

    "MARCADORES_TUMORALES": {
        "nombres": [
            "MARCADORES TUMORALES", "MARCADORES CANCER", "MARCADORES ONCOLOGICOS",
            "MARCADORES NEOPLASICOS", "PANEL TUMORAL"
        ],
        "componentes": [
            "CEA", "AFP", "CA 125", "CA 15-3", "CA 19-9", "PSA TOTAL", 
            "PSA LIBRE", "BETA2 MICROGLOBULINA", "HCG", "CA 72-4",
            "CYFRA 21-1", "NSE", "SCC", "CROMOGRANINA A", "CALCITONINA",
            "INDICE PSA LIBRE/TOTAL", "HE4", "ROMA"
        ]
    },

    "AUTOINMUNIDAD": {
        "nombres": [
            "AUTOINMUNIDAD", "ENFERMEDADES AUTOINMUNES",
            "ANTICUERPOS AUTOINMUNES"
        ]
    },

    "MICROBIOLOGIA": {
        "nombres": [
            "MICROBIOLOGIA", "MICROBIOLÓGICO", "MICROBIANO",
            "ESTUDIO MICROBIOLOGICO", "CULTIVO BACTERIOLOGICO",
            "SEROLOGIA", "SCREENING MICROBIOLOGICO",
            "ANALISIS MICROBIOLOGICO", "MUESTRA MICROBIOLOGICA"
        ],
        "componentes": [
            "HEPATITIS B", "HEPATITIS C", "HIV", "VDRL",
            "CULTIVO", "ANTIGENO", "ANTICUERPO", "PCR",
            "IGG", "IGM", "ELISA", "WESTERN BLOT",
            "BACTERIAS", "HONGOS", "PARASITOS",
            "NO REACTIVO", "REACTIVO", "POSITIVO", "NEGATIVO"
        ]
    },

    "SEROLOGIA": {
        "nombres": [
            "SEROLOGIA", "PRUEBAS SEROLOGICAS", "SCREENING",
            "TEST SEROLOGICO", "INMUNOLOGIA", "TEST RAPIDO",
            "MUESTRA SEROLOGICA", "ANALISIS SEROLOGICO"
        ],
        "componentes": [
            "ANTICUERPOS", "ANTIGENOS", "IGG", "IGM",
            "ELISA", "WESTERN BLOT", "SCREENING",
            "NO REACTIVO", "REACTIVO", "POSITIVO", "NEGATIVO"
        ]
    },

    "EXAMEN_GENERAL": {
        "nombres": [
            "LABORATORIO", "EXAMEN", "ANALISIS", "MUESTRA",
            "ESTUDIO", "TEST", "RESULTADO", "INFORME"
        ],
        "componentes": [
            "MUESTRA", "RESULTADO", "METODO", "TECNICA",
            "VALOR", "REFERENCIA", "UNIDAD", "OBSERVACION"
        ]
    },
    
    "BIOQUIMICA_SANGUINEA": {
        "nombres": [
            "BIOQUIMICA SANGUINEA", "ELECTROLITOS", 
            "QUIMICA SANGUINEA"
        ],
        "componentes": [
            "ELECTROLITO POTASIO", "ELECTROLITO CLORO",
            "POTASIO", "CLORO", "K", "CL"
        ]
    }
}