from src.ingestion.vector_store import *
from utils.embeding_model import embeding_model

class Retriever:
    def __init__(self):
        pass

    def basic_retriever(self):
        try:
            pass
        except Exception as e:
            logger.error("Error hapening while retrieving the vector store")
            raise CustomExeption("Error hapening while retrieving the vector store",e)