import uuid
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
from src.retrieval.context_builder import ContextBuilder
from src.retrieval.retriever import Retriever
#from llm.llm_client import LlmClient
from src.answer_genaration.response_genarater import ResponseGenarater
from utils.embeding_model import gemini_model
from src.agents.custom_agents import CustomAgents
from mongo_db.mongo_client import MongoClientProvider
from mongo_db.evaluation_repo import EvaluationRepository
from mongo_db.evaluation_service import EvaluationService
from dotenv import load_dotenv
from langchain_classic.retrievers import MergerRetriever

load_dotenv()

if __name__=="__main__":
    retrieve = Retriever()
    memory = ChatMemory()

    mongo_provider = MongoClientProvider(
        uri= os.getenv("CONNECTION_STRING"),
        db_name = "rag_observability"
    )

    ragas_repo = EvaluationRepository(mongo_provider.get_db())
    ragas_service = EvaluationService(ragas_repo)



    final_retriever = retrieve.basic_retriever()
    llm = gemini_model()
    agents = CustomAgents(llm)

    retry_limit = 2
    
    while True:
        run_id = 0
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
            while retry_limit < 2:
                print("Low confidence answer. Retrying with expanded query")
                
                expanded_query = rewritten_query+" detail explanation example..."
                docs = final_retriever.invoke(expanded_query)
                context=context_builder.build(docs)
                answer = response_genarator.genarate(query,context)

                retry_limit+=1

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

        ragas_service.evaluation_and_store(
            run_id=run_id,
            query=query,
            rewritten_query=rewritten_query,
            answer=answer,
            contexts=contexts,
            ragas_results=results,
            metadata={
                    "retriever": "bm25 + chroma + rrf",
                    "reranker": "bge-reranker-large",
                    "embedding_model": "all-MiniLM-L6-v2",
                    "llm": "gemini",
                    "chunk_size": 512,
                    "top_k": 8
                }
        )
        run_id +=1