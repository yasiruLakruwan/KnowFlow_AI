from langchain_core.documents import Document
from exeption import CustomExeption
from logger import get_logger
from langchain_chroma import Chroma
from config.path_config import presist_dir,document_pkl
from utils.embeding_model import embeding_model
import os
import pickle
 


logger = get_logger(__name__)    

def convert_chunks_to_documents(chunks):
    docs=[]

    for chunk in chunks:
        docs.append(
            Document(
                page_content=chunk["content"],
                metadata = {
                    "id":chunk["id"],
                    "source":chunk["source"],
                    "section":chunk["section"] 
                }
            )
        )
    return docs

def load_vector_store():
    try:    
        logger.info("Loading existing vector database......")
        embed_model = embeding_model()

        db = Chroma(
            persist_directory=presist_dir,
            embedding_function=embed_model
        )
        logger.info("db loaded successfully....")

        return db
    
    except Exception as e:
        raise CustomExeption("Error loading the vector db",e)
    
def load_documets_for_bm25(document_pkl:str):
    try:
        file_path = os.path.join(document_pkl,"all_documents.pkl")
        if not os.path.exists(file_path):
            raise CustomExeption(f"File path {file_path} doesnot exists")
        with open(file_path,"rb") as f:
            documents = pickle.load(f)
        return documents
    
    except Exception as e:
        raise CustomExeption("Error hapening in load document.pkl file")

if __name__== "__main__":
    db = load_vector_store()
    print(db) 
    documents = load_documets_for_bm25(document_pkl)
    print(len(documents)) 