from directry_loader import DirectryLoader
from chunker import TextChunking
from embedder import EmbeddingGenarater
from config.path_config import *
from exeption import CustomExeption
from logger import get_logger


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
            
            for filename,text in sections :
                chunks = chunker.chunk_section(text)

                logger.info("adding metadata to the chunks.....")
                for chunk in chunks:
                    chunks_with_meta = chunker.chunk(chunk,filename)
                    all_chunks.append(chunks_with_meta)

        logger.info(f"Created all chunks {len(all_chunks)}")
        return all_chunks
    
    except Exception as e:
        raise CustomExeption(f"Error running the ingestion pipeline....",e)


if __name__=="__main__":
    pipeline() 

