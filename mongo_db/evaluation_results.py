from datetime import datetime
from typing import Dict

# Creating schema......

def evaluation_document(
        run_id:str,
        question:str,
        answer:str,
        scores: Dict[str,float],
        metadata: Dict
):
    return {
        "run_id":run_id,
        "question":question,
        "answer":answer,
        "scores":scores,
        "metadata": metadata,
        "created_at":datetime.utcnow()
    }