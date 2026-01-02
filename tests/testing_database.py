import os
from mongo_db.mongo_client import MongoClientProvider
from dotenv import load_dotenv
from mongo_db.evaluation_service import EvaluationService
from mongo_db.evaluation_repo import EvaluationRepository
load_dotenv()

def testing():
    uri = os.getenv("CONNECTION_STRING")
    # db = "rag_observability"
    mongo_client = MongoClientProvider(
        uri=uri,
        db_name="rag_observability"
    )
    repo = EvaluationRepository(mongo_client.get_db())
    service = EvaluationService(repo)

    print(f"Initialize mongo client {mongo_client}")

    run_id = 1
    query = "what is the mostly used machine learning model"
    rewritten_query = "what is the most used machine learning model for production exept testing datasets... "
    answer = "The most used machine learning model is SVM"
    contexts = "these are the contexts."
    ragas_results = {
        'context_precision': 0.0000, 'faithfulness': 1.0000, 'answer_relevancy': 0.0000
        }
    metadata={
                    "retriever": "bm25 + chroma + rrf",
                    "reranker": "bge-reranker-large",
                    "embedding_model": "all-MiniLM-L6-v2",
                    "llm": "gemini",
                    "chunk_size": 512,
                    "top_k": 8
                }
    
    service.evaluation_and_store(
            run_id=run_id,
            query=query,
            rewritten_query=rewritten_query,
            answer=answer,
            contexts=contexts,
            ragas_results=ragas_results,
            metadata=metadata
    )

    print(f"save data to database")
    """
    ragas_service.evaluation_and_store(
            run_id=run_id,
            query=query,
            rewritten_query=rewritten_query,
            answer=answer,
            contexts=contexts,
            ragas_results=results,
            metadata={
                    "retriever": "bm25 + chroma + rrf",
                    "reranker": "bge-reranker-large",
                    "embedding_model": "all-MiniLM-L6-v2",
                    "llm": "gemini",
                    "chunk_size": 512,
                    "top_k": 8
                }
        )
    """





if __name__=="__main__":
    testing()