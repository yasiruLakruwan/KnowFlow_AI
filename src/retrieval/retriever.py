from src.chat_memory.chat_history import ChatMemory
from src.ingestion.vector_store import *
from utils.embeding_model import embeding_model
from utils.helper_functions import load_vector_store, load_documets_for_bm25,build_ragas_dataset, rewrite_query,run_ragas
from config.path_config import *
# langchain_community.retrievers import MergerRetriever
from langchain_community.retrievers import BM25Retriever
from langchain_community.cross_encoders import HuggingFaceCrossEncoder
from langchain_classic.retrievers.document_compressors import CrossEncoderReranker
from langchain_classic.retrievers import ContextualCompressionRetriever
from context_builder import ContextBuilder
#from llm.llm_client import LlmClient
from src.answer_genaration.response_genarater import ResponseGenarater
from utils.embeding_model import gemini_model
from src.agents.custom_agents import CustomAgents

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
        
        return docs

if __name__=="__main__":
    retrieve = Retriever()
    memory = ChatMemory()

    final_retriever = retrieve.basic_retriever()
    llm = gemini_model()
    agents = CustomAgents(llm)

    while True:
        query = input("How may I help you: ")

        if query.lower() in ["exit","quit"]:
            print("Thank you...Have a nice day..!")
            break

        memory.user_messages(query)

        # Planer deside what to do

        action = agents.plan_aciton(
            # llm = llm,
            question = query,
            chat_history = memory.get()
        )

        # Query handling according based on the plan

        if action=="rewrite_and_retrieve":
            # rewriting query.....
            rewrite_query = rewrite_query(
                llm = llm,
                question=query,
                chat_history=memory.get()
            )
        else:
            rewritten_query = query

        # Retrival (SAME retriever..)
        docs = retrieve.test_retrival(
            final_retriever,
            rewritten_query
        )

        # Build context
        context_builder = ContextBuilder(max_tokens=3000)

        # Getting contexts for the ragas evaluation 

        contexts = [doc.page_content for doc in docs]

        context = context_builder.build(docs)

        print("\n====Context sent to LLM=====")
        print(context)

        response_genarator = ResponseGenarater()

        print("======Answer======")
        answer = response_genarator.genarate(query,context)

        # Critic verification...
        critique = agents.critique(
            # llm = llm,
            question=query,
            context=context,
            answer=answer
        )

        # Retry if fails(Agentic loop)
        if critique == "FAIL":
            print("Low confidence answer. Retrying with expanded query")
            
            expanded_query = rewritten_query+" detail explanation example..."
            docs = final_retriever.invoke(expanded_query)
            context=context_builder.build(docs)
            answer = response_genarator.genarate(query,context)

        memory.add_ai_message(answer)

        print(answer)


        print("======RAGAS evaluation======")

        dataset = build_ragas_dataset(
            user_inputs=[query],
            responses=[answer],
            retrieved_contexts=[contexts],
            references=[""]  # dummy reference
        )
        
        # ragas evaluation 

        results = run_ragas(dataset,llm)
        print(results)
        logger.info(f"RAGAS results are: {results}")



