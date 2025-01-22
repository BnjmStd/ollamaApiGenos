# chat/app/services/query_service.py
from typing import Dict, List
from .guide_service import GuideService
from .services import OllamaService

class QueryService:
   def __init__(self):
       self.guide_service = GuideService()
       self.ollama_service = OllamaService()

   async def process_query(self, question: str) -> Dict:
       # Buscar secciones relevantes
       relevant_sections = self.guide_service.search_by_keywords(question)
       
       # Crear contexto para Llama2
       context = self._format_context(relevant_sections)

       # Obtener respuesta
       response = await self.ollama_service.get_response(
           question=question,
           context=context
       )

       return {
           "response": response,
           "sources": relevant_sections
       }

   def _format_context(self, sections: List[Dict]) -> str:
       return "\n\n".join([
           f"Sección: {section['section']}\n{section['content']}" 
           for section in sections
       ])