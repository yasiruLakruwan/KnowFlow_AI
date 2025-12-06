import re 
from typing import List
from exeption import CustomExeption
from logger import get_logger

logger = get_logger(__name__)


class TextChunking:
    def __init__(self,max_chunk_size:int=700,overlap:int=70):
        self.max_chunk_size = max_chunk_size
        self.overlap = overlap
    
    def split_into_sections(self, text: str) -> List[str]:
        """
        Split by heading to keep sementic structure.
        """
        try:
            logger.info("Start section spliting...")

            pattern = r"\n(?=(?:[A-Z][A-Za-z0-9 ]{3,}\n))"  # headings in PDF
            sections = re.split(pattern,text)
            return [s.strip() for s in sections if s.strip()]
        
        except Exception as e:
            logger.error(f"Error while sections spliting")
            raise CustomExeption(f"Error while spliting sections",e)
        
    def chunk_section(self,section: str) ->List[str]:
        """
        Break sections into smaller chunks of controlled size.
        """
        try:
            logger.info("Start chunking...")
            chunks = []
            words = section.split()

            current_chunk = []

            for word in words:
                current_chunk.append(word)
                if len(" ".join(current_chunk)) >= self.max_chunk_size:
                    chunks.append(" ".join(current_chunk))
                    current_chunk = current_chunk[-self.overlap:]
            
            if current_chunk:
                chunks.append(" ".join(current_chunk))

            return chunks   
        except Exception as e:
            logger.error(f"Error while chunking....")
            raise CustomExeption(f"Error while data chunking",e)
        
    def chunk(self,text:str)->List[str]:
        """
        Full pipeline
        1. Split by semantic section
        2. Chunk cleanly
        """
        all_chunks = []
        sections = self.split_into_sections(text)

        for section in sections:
            all_chunks.extend(self.chunk_section(section))
        
        return all_chunks

if __name__=="__main__":
    chunker = TextChunking(700,70)
    sample_text = """
        INTRODUCTION
            This is a simple explanation text that goes on and on. 
            We are testing chunking. It should split into multiple chunks 
            based on the max chunk size.

        SYSTEM DESIGN
            This section explains how the system works. It contains architecture 
            diagrams and more documentation.
    """

    all_chunks = chunker.chunk(sample_text)
    for i,chunk in enumerate(all_chunks):  
       if i<=2:  
        print(f"section: {i+1}------")
        print(chunk)