from pydantic import BaseModel
from typing import List,Optional,Dict

class ChatRequest(BaseModel):
    query:str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    session_id:str
    answer: str
    rewritten_query:str
    contexts: List[str]
    ragas:Dict
    