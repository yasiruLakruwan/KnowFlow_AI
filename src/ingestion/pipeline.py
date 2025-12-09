from directry_loader import DirectryLoader
from chunker import TextChunking
from embedder import EmbeddingGenarater
from config.path_config import *
from exeption import CustomExeption
from logger import get_logger
from utils.embeding_model import embeding_model,gemini_model
from vector_store import VectorStore
from langchain_chroma import Chroma


logger = get_logger(__name__)

def pipeline():
    try:
        # Directry loader
        logger.info("Directry loading......")
        loader = DirectryLoader(data_dir)
        logger.info("Directry loaded.......")

        logger.info("Start loader.load funcion......")
        documents = loader.load()

        logger.info("Initialized chunker......")
        chunker = TextChunking(700,70)

        all_chunks =[]
        
        logger.info("Testing document structure......")
        for index,item in enumerate(documents):
            """if index<2 :
                print(f"----------Document--{index+1}--------")
                print(f"filename---------{item['filename']}---------------") 
                print(f"content---------{item['content'][:500]}---------------")"""
            
            content = item['content']
            filename = item['filename']

            logger.info(f"Processing file {filename}")
            logger.info("Start splitting into sections")
            
            sections = chunker.split_into_sections(content)

            logger.info("Getting sections and chunk sections....")
            
            for header,body in sections :
                chunks = chunker.chunk_section(body)

                logger.info("adding metadata to the chunks.....")
                for chunk in chunks:
                    chunks_with_meta = chunker.chunk(chunk,header)
                    all_chunks.append(chunks_with_meta)

        logger.info(f"Created all chunks {len(all_chunks)}")
        print(type(all_chunks))
        #return all_chunks

        # Doing emberdings......
        try:
            logger.info("initialized models")
            embedding_molel = embeding_model()
            # geminii_model = gemini_model()

            vector_db = VectorStore(presist_dir,embedding_molel,all_chunks)

            logger.info("Create vectorstore....")
            vector_db.create_vector_store()

            logger.info("Adding chunks to chroma db...")

            """---from here need to build----"""
            
            
        except Exception as e:
            logger.error("Error happening embeddings")
            raise CustomExeption(f"Error happening in embeddings") 
    
    except Exception as e:
        raise CustomExeption(f"Error running the ingestion pipeline....",e)


if __name__=="__main__":
    pipeline() 

