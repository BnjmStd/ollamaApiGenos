from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field

class ChatQuery(BaseModel):
    question: str
    context_type: Optional[str] = Field(default=None, description="guide/exam/report")
    document_id: Optional[str] = None