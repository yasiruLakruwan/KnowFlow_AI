from src.ingestion.vector_store import *
from utils.embeding_model import embeding_model
from utils.helper_functions import load_vector_store, load_documets_for_bm25
from config.path_config import *
# langchain_community.retrievers import MergerRetriever
from langchain_community.retrievers import BM25Retriever
from langchain_community.cross_encoders import HuggingFaceCrossEncoder
from langchain_classic.retrievers.document_compressors import CrossEncoderReranker
from langchain_classic.retrievers import ContextualCompressionRetriever

from langchain_classic.retrievers import MergerRetriever

class Retriever:
    def __init__(self):
        self.db = None

    def basic_retriever(self):
        try:
            logger.info("loading the vectorstore")
            self.db = load_vector_store()
            retriever = self.db.as_retriever(
                search_type = "similarity_score_threshold",
                search_kwargs = {
                    "k":8,
                    "score_threshold":0.2
                }
            )
            # Add bm25 retriever
            logger.info("Adding bm25 retriever...")
            all_docs = load_documets_for_bm25(document_pkl)
            bm25 = BM25Retriever.from_documents(all_docs)
            bm25.k = 8
        
            # Combine retrievers using RRF(Production approach)
            logger.info("Combine retrievers using RRF(Production approach)")
            hybrid_retriever = MergerRetriever(
                retrievers = [retriever,bm25],
                merge_mode = "rrf",
                weights = [0.5,0.5]
            )

            # Add BGE reranker (Second-stage reranking)
            logger.info("Add BGE reranker (Second-stage reranking)")
            cross_encoder = HuggingFaceCrossEncoder(model_name = "BAAI/bge-reranker-large")
            compressor = CrossEncoderReranker(
                    model=cross_encoder,
                    top_n=4
                )

            final_retriever = ContextualCompressionRetriever(
                base_retriever = hybrid_retriever,
                base_compressor = compressor
            )

            return final_retriever
        
        except Exception as e:
            logger.error("Error hapening while retrieving the vector store")
            raise CustomExeption("Error hapening while retrieving the vector store",e)
        
    def test_retrival(self,retriever,query):
        docs = retriever.invoke(query)

        print(f"\n🔍 Query: {query}")
        print(f"📄 Retrieved {len(docs)} documents\n")

        for i, doc in enumerate(docs):
            print(f"--- Result {i+1} ---")
            print("Metadata:", doc.metadata)
            print("Content:", doc.page_content[:300])
            print()
    

if __name__=="__main__":
    retrieve = Retriever()
    final_retriever = retrieve.basic_retriever()

    retrieve.test_retrival(
        final_retriever,
        "How to sample the data?"
    )