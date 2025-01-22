# chat/app/services/guide_service.py
from pathlib import Path
import json
from typing import List, Dict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class GuideService:

    def __init__(self, guides_path: Path = Path("guides")):
        self.guides_path = guides_path
        self.guides = {}
        self.load_guides()
        
        # Inicializar vectorizador con el contenido
        texts = []
        for guide in self.guides.values():
            for section in guide['secciones']:
                texts.append(section['contenido'])
        
        self.vectorizer = TfidfVectorizer()
        if texts:  # Solo ajustar si hay textos
            self.vectorizer.fit(texts)

    def load_guides(self):
        """Cargar guías desde archivos JSON"""
        if not self.guides_path.exists():
            self.guides_path.mkdir(parents=True)
        
        for file in self.guides_path.glob("*.json"):
            with open(file, 'r', encoding='utf-8') as f:
                self.guides[file.stem] = json.load(f)

    def search_by_keywords(self, query: str, limit: int = 3) -> List[Dict]:
        results = []
        query_vector = self.vectorizer.transform([query])
        
        for guide_id, guide in self.guides.items():
            for section in guide['secciones']:
                section_vector = self.vectorizer.transform([section['contenido']])
                similarity = cosine_similarity(query_vector, section_vector)[0][0]
                
                if similarity > 0.1:  # Umbral mínimo de similitud
                    results.append({
                        'guide_id': guide_id,
                        'section': section['titulo'],
                        'content': section['contenido'],
                        'similarity': similarity
                    })
        
        return sorted(results, key=lambda x: x['similarity'], reverse=True)[:limit]