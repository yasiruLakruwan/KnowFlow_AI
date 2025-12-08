from directry_loader import DirectryLoader
from chunker import TextChunking
from embedder import EmbeddingGenarater
from config.path_config import *

class main:
    def pipeline(self):
        # Directry loader
        loader = DirectryLoader(data_dir)

        documents = loader.load()

        # Text chunking
        for item in enumerate(documents):
           file_name =  item['filename']
           conent = item['content']
           chunker = TextChunking(700,70)
        
           sections = chunker.split_into_sections(conent)
           
           for section in sections:
               chunks = chunker.chunk_section(section)

               for chunk in chunks:
                  all_chunks = chunker.chunk(chunk,file_name)

