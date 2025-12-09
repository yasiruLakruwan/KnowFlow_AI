from langchain_core.documents import Document

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