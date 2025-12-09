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

            pattern = r"\n\s*(?P<header>[A-Z][A-Za-z0-9 ]{3,})\s*\n"   # headings in PDF
            matches = list(re.finditer(pattern,text))

            sections = []

            for i,match in enumerate(matches):
                start = match.end()
                end = matches[i+1].start() if i+1 < len(matches) else len(text) 

                header = match.group("header").strip()
                body = text[start:end].strip()

                sections.append((header,body))   

            return sections
        
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
        
    def chunk(self,text:str,source:str)->List[str]:
        """ Chunking the sections and section body.. """
        all_chunks= []
        sections = self.split_into_sections(text)

        chunk_index = 0
        source_name = source.replace(".pdf"," ").replace(" ","_")
        # adding metadata....
        for section_title,section_text in sections:
            chunked_texts = self.chunk_section(section_text)
            for chunk_text in chunked_texts:
                all_chunks.append({
                    "id":f"{source_name}-chunk-{chunk_index}",
                    "section":section_title,
                    "source":source_name,
                    "content":chunk_text
                })

                chunk_index += 1

        return all_chunks
    
# Testing the class........

'''if __name__=="__main__":

    chunker = TextChunking(700,70)
    sample_text = """
        #INTRODUCTION
        #    This is a simple explanation text that goes on and on. 
        #    We are testing chunking. It should split into multiple chunks 
        #    based on the max chunk size.

        #SYSTEM DESIGN
        #    This section explains how the system works. It contains architecture 
        #    diagrams and more documentation.
    """

    all_chunks = chunker.chunk(sample_text,"System Design Document.pdf")
    for i,chunk in enumerate(all_chunks):  
       if i<=2:  
        print(f"section: {i+1}------")
        print(chunk) '''
        