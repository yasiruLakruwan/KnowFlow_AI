import os
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from logger import get_logger
from utils.embeding_model import embeding_model,gemini_mode
from exeption import CustomExeption
from config.path_config import presist_dir

logger = get_logger(__name__)

# Creating vectorstore

class VectorStore:
    def __init__(self,presist_dir,embeding_model):
        self.presist_dir = presist_dir
        self.embeding_model = embeding_model
    
    def create_vector_store(self):
        try:
            logger.info("Vector db initialized.....")
            # Create vector store
            if os.path.exists(presist_dir):
                print(f"Vectordb exist in {presist_dir}")
            else:
                os.makedirs(presist_dir,exist_ok=True)

                db = Chroma(
                    embedding_function=self.embeding_model,
                    presist_dir = self.presist_dir
                )
            return db
        
        except Exception as e:
            logger.error(f"Error happened when initialized the vector db.....")
            raise CustomExeption(f"Error while embedings",e)
