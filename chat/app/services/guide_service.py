from pathlib import Path 
import json
from typing import List, Dict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from loguru import logger

class GuideService:
    def __init__(self, guides_path: Path = None):
        # Obtener ruta absoluta desde app/
        if guides_path is None:
            base_dir = Path(__file__).parent.parent  # sube un nivel desde services/ a app/
            self.guides_path = base_dir / "guides"
        else:
            self.guides_path = guides_path
            
        logger.info(f"Usando directorio de guías: {self.guides_path.absolute()}")
        
        self.guides = {}
        self.vectorizer = TfidfVectorizer()
        self.load_guides()
        self._create_index()

    def load_guides(self):
        """Cargar guías desde archivos JSON"""
        if not self.guides_path.exists():
            self.guides_path.mkdir(parents=True)
        
        for file in self.guides_path.glob("*.json"):
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    guide = json.load(f)
                    self.guides[guide['id']] = guide
                    logger.info(f"Guía cargada: {guide['id']}")
            except Exception as e:
                logger.error(f"Error cargando guía {file}: {e}")

    def _create_index(self):
        """Crear índices para búsqueda"""
        texts = []
        self.section_mapping = []

        for guide_id, guide in self.guides.items():
            # Asegurar que hay textos para vectorizar
            if not guide.get('secciones'):
                continue
                
            # Indexar información general
            guide_info = f"{guide['nombre']} {guide['descripcion']}"
            texts.append(guide_info)
            self.section_mapping.append({
                'guide_id': guide_id,
                'guide_name': guide['nombre'],
                'section_id': 'info',
                'section_title': 'Información General'
            })

            # Indexar secciones
            self._process_sections(guide_id, guide['nombre'], guide['secciones'], texts)

        # Solo ajustar vectorizador si hay textos
        if texts:
            self.vectorizer = TfidfVectorizer()
            self.vectors = self.vectorizer.fit_transform(texts)
            logger.info(f"Vectorizador inicializado con {len(texts)} textos")
        else:
            logger.warning("No se encontraron textos para vectorizar")

    def _process_sections(self, guide_id: str, guide_name: str, sections: List[Dict], texts: List[str], parent_title: str = ""):
        """Procesar secciones y subsecciones recursivamente"""
        for section in sections:
            if section['contenido']:
                texts.append(section['contenido'])
                self.section_mapping.append({
                    'guide_id': guide_id,
                    'guide_name': guide_name,
                    'section_id': section['id'],
                    'section_title': f"{parent_title}{section['titulo']}",
                    'type': 'section'
                })

            # Procesar subsecciones si existen
            if 'subsecciones' in section and section['subsecciones']:
                self._process_sections(
                    guide_id, 
                    guide_name,
                    section['subsecciones'],
                    texts,
                    f"{parent_title}{section['titulo']} > "
                )

    def search_by_keywords(self, query: str, limit: int = 3) -> List[Dict]:
        """Búsqueda por palabras clave con contexto mejorado"""
        try:
            results = []
            query_vector = self.vectorizer.transform([query])
            
            similarities = cosine_similarity(query_vector, self.vectors)[0]
            
            # Obtener índices de los resultados más relevantes
            top_indices = np.argsort(similarities)[-limit:][::-1]
            
            for idx in top_indices:
                if similarities[idx] > 0.1:  # Umbral mínimo de similitud
                    mapping = self.section_mapping[idx]
                    guide = self.guides[mapping['guide_id']]
                    
                    # Encontrar el contenido correspondiente
                    content = self._find_section_content(guide, mapping['section_id'])
                    
                    results.append({
                        'guide_id': mapping['guide_id'],
                        'guide_name': mapping['guide_name'],
                        'section': mapping['section_title'],
                        'content': content,
                        'similarity': float(similarities[idx])
                    })

            return results

        except Exception as e:
            logger.error(f"Error en búsqueda: {e}")
            return []

    def _find_section_content(self, guide: Dict, section_id: str) -> str:
        """Encontrar contenido de una sección por su ID"""
        def search_recursive(sections):
            for section in sections:
                if section['id'] == section_id:
                    return section['contenido']
                if 'subsecciones' in section:
                    result = search_recursive(section['subsecciones'])
                    if result:
                        return result
            return None

        if section_id == 'info':
            return f"{guide['nombre']}\n{guide['descripcion']}"
        
        return search_recursive(guide['secciones']) or ""