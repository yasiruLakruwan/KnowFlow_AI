class EvaluationRepository:
    def __init__(self,db):
        self.collection = db["ragas_evaluations"]
    
    def save(self,document:dict):
        self.collection.insert_one(document)
    
    def find_by_run(self,run_id:str):
        return list(self.collection.find({"run_id" : run_id}))
    

    # DB isolated 
    # Replace Mongo later if needed
    # Clean architecture