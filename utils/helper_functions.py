from langchain_core.documents import Document
from neo4j import GraphDatabase
from exeption import CustomExeption
from logger import get_logger
from langchain_chroma import Chroma
from config.path_config import presist_dir
from utils.embeding_model import embeding_model
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
        return db
    except Exception as e:
        raise CustomExeption("Error loading the vector db",e)
    

if __name__=="__main__":
    db = load_vector_store()
