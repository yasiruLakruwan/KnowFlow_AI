class EvaluationRepository:
    def __init__(self,db):
        self.collection = db["ragas_evaluations"]