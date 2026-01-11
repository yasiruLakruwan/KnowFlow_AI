from pydantic import BaseModel,ConfigDict
from typing import List,Optional,Dict

class ChatRequest(BaseModel):
    query:str
    session_id: Optional[str] = None

class RagasMatrics(BaseModel):
    context_precision: float
    context_recall:float
    faithfulness: float
    answer_relevancy: float

    model_config = ConfigDict(extra="allow")

class ChatResponse(BaseModel):
    session_id:str
    answer: str
    rewritten_query:str
    contexts: List[str]
    #ragas:RagasMatrics

    