import uuid
from fastapi import APIRouter,Depends
from app.schemas.chat import ChatRequest,ChatResponse, RagasMatrics
from app.dependancies import get_rag_service
from app.service.rag_service import RagSevice

router = APIRouter()


@router.get("/home")
# Home route for the API.......
def home():
    return "Welcome to rag application.......!"


@router.post("/chat",response_model=ChatResponse)

def chat(
    payload:ChatRequest,
    rag_service:RagSevice = Depends(get_rag_service)
):
    session_id = payload.session_id or str(uuid.uuid4) 

    result = rag_service.chat(
        query=payload.query,
        session_id=session_id
    )
    return ChatResponse(
        session_id=session_id,
        answer=result["answer"],
        rewritten_query=result["rewritten_query"],
        contexts=result["contexts"],
        #ragas=RagasMatrics(**result["ragas"])
    )

@router.get("/chat/{session_id}")
def get_chat(session_id:str,rag_service:RagSevice=Depends(get_rag_service)):
    memory = rag_service.memory_store.get(session_id)
    
    if not memory:
        return f"Can not find {session_id}"
    return {
        "session_id": session_id,
        "messages": memory.get()
    }
