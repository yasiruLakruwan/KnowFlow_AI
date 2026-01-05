from datetime import datetime
from typing import Dict
import uuid

# Creating schema......

def evaluation_document(
        run_id:str,
        query:str,
        rewritten_query:str,
        answer:str,
        contexts:str,
        ragas_results:Dict,
        metadata: Dict 
):
    return {
        "run_id":run_id or str(uuid.uuid4()),
        "question":query,
        "rewritten_query":rewritten_query,
        "answer":answer,
        "contexts":contexts,
        "scores":ragas_results,
        "metadata": metadata,
        "created_at":datetime.utcnow()
    }