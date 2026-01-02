from mongo_db.evaluation_results import evaluation_document
from mongo_db.evaluation_repo import EvaluationRepository
 
class EvaluationService:
    def __init__(self,repo:EvaluationRepository):
        self.repo = repo

    def evaluation_and_store(
            self,
            run_id,
            query,
            rewritten_query,
            answer,
            contexts,
            ragas_results,
            metadata
    ):
        doc = evaluation_document(
            run_id,
            query,
            rewritten_query,
            answer,
            contexts,
            ragas_results,
            metadata
        )
        self.repo.save(doc)






