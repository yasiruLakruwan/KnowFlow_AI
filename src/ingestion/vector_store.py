import os
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from logger import get_logger
from utils.embeding_model import embeding_model,gemini_model
from exeption import CustomExeption
from config.path_config import presist_dir
from langchain_core.documents import Document
from utils.helper_functions import convert_chunks_to_documents
logger = get_logger(__name__)

# Creating vectorstore

class VectorStore:
    def __init__(self,presist_dir,embeding_model,chunks):
        self.presist_dir = presist_dir
        self.embeding_model = embeding_model
        self.db = None    # Store Chroma instance
        self.chunks = chunks
    
    def create_vector_store(self):
        try:
            logger.info("Vector db initialized.....")
            # Create vector store
            documents = convert_chunks_to_documents(self.chunks)

            if os.path.exists(self.presist_dir) and len(os.listdir(self.presist_dir)) > 0:
                logger.info("✅ Vector store already exists. No need to re-process documents.")
                 
                self.db = Chroma(
                    persist_directory=self.presist_dir,
                    embedding_function=self.embeding_model, 
                    #collection_metadata={"hnsw:space": "cosine"}
                )
                print(f"Loaded existing vector store with {self.db._collection.count()} documents")
                return self.db
            
            # create a new db
            os.makedirs(self.presist_dir,exist_ok=True)
            
            self.db = Chroma.from_documents(
                documents=documents,
                embedding=self.embeding_model,
                persist_directory = self.presist_dir
            )
            
            return self.db 

        except Exception as e:
            logger.error(f"Error happened when initialized the vector db.....")
            raise CustomExeption(f"Error while embedings",e)
    
    