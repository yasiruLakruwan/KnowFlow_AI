import re 
from typing import List

class TextChunking:
    def __init__(self,max_chunk_size:int=700,overlap:int=70):
        self.max_chunk_size = max_chunk_size
        self.overlap = overlap
    def split_into_sections(self, text: str) -> List[str]:
        """
        Split by heading to keep sementic structure.
        """
        pattern = r"\n(?=(?:[A-Z][A-Za-z0-9 ]{3,}\n))"  # headings in PDF
        sections = re.split(pattern,text)

        return [s.strip() for s in sections if s.strip()]
    
    def chunk_section(self,section: str) ->List[str]:
        """
        Break sections into smaller chunks of controlled size.
        """

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
