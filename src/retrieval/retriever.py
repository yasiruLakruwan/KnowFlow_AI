from src.ingestion.vector_store import *
from utils.embeding_model import embeding_model
from utils.helper_functions import load_vector_store

class Retriever:
    def __init__(self):
        self.db = None

    def basic_retriever(self):
        try:
            self.db = load_vector_store()
            retriever = self.db.as_retriever(
                search_type = "similarity",
                search_kwargs = {
                    "k":8,
                    "score_threshold":0.2
                }
            )
        except Exception as e:
            logger.error("Error hapening while retrieving the vector store")
            raise CustomExeption("Error hapening while retrieving the vector store",e)