from pydantic import BaseModel
from typing import List, Optional

class ChatRequest(BaseModel):
    query: str
    top_k: int = 5
    model: str = "gemini-2.5-flash"
    session_id: Optional[str] = None
    doc_filter: Optional[List[str]] = None
    only_if_sources: bool = False
