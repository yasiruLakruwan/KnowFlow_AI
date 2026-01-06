import os
from mongo_db.mongo_client import MongoClientProvider
from mongo_db.evaluation_repo import EvaluationRepository
from mongo_db.evaluation_service import EvaluationService
from app.service.rag_service import RagSevice
from dotenv import load_dotenv

load_dotenv()

def get_rag_service():
    mongo_provider = MongoClientProvider(
        uri=os.getenv("CONNECTION_STRING"),
        db_name="rag_observability"
    )