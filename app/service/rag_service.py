import os
import uuid
from src.chat_memory.chat_history import ChatMemory
from src.retrieval.retriever import Retriever
from src.retrieval.context_builder import ContextBuilder
from src.answer_genaration.response_genarater import ResponseGenarater
from src.agents.custom_agents import CustomAgents
from utils.helper_functions import (
    build_ragas_dataset,
    rewrite_query,
    run_ragas
)
from utils.embeding_model import gemini_model
from mongo_db.evaluation_service import EvaluationService

class RagSevice:
    def __init__(self,evaluation_service:EvaluationService):
        self.retrieve = Retriever()
        self.llm = gemini_model()
        self.agents = CustomAgents(self.llm)
        self.evaluation_service = evaluation_service
        self.retry_limit = None

        # Session id -> ChatMemory
        self.memory_store = {}

    def _get_memory(self,session_id:str):
        if session_id not in self.memory_store:
            self.memory_store[session_id] = ChatMemory()
        return self.memory_store[session_id] 
    
    def chat(self,query:str,session_id:str):
        memory = self._get_memory(session_id)
        memory.user_messages(query)

        # Agent planing

        self.retry_limit = 2

        action = self.agents.plan_action(
            question = query,
            chat_history = memory.get()
        )

        if action == "rewrite_and_retrieve":
            while self.retry_limit<2:
                rewritten_query = rewrite_query(
                    llm=self.llm,
                    question=query,
                    chat_history=memory.get()
                ) 
        else:
            rewritten_query = query

        # ------------Retrieval------------

        retriever = self.retrieve.basic_retriever()
        docs = self.retrieve.test_retrival(retriever,rewritten_query)

        contexts = [doc.page_content for doc in docs]
        context_builder = ContextBuilder(max_tokens=3000)

        context = context_builder.build(docs)

        #------Answer-------

        responce_genarator = ResponseGenarater()
        answer = responce_genarator(query,context)
        critique = self.agents.critique(
            question = query,
            context = context,
            answer = answer
        )
        memory.add_ai_message(answer)

        #--------RAGAS-------

        dataset = build_ragas_dataset(
            user_inputs=[query],
            responses=[answer],
            retrieved_contexts=[contexts],
            references=[""]
        )

        ragas_results = run_ragas(dataset,self.llm)
        
        self.evaluation_service.evaluation_and_store(
            run_id=None or str(uuid.uuid4()),
            query = query,
            rewritten_query=rewritten_query,
            answer = answer,
            contexts =contexts,
            ragas_results=ragas_results,
            metadata = {
                "retriever": "bm25 + chroma + rrf",
                "reranker": "bge-reranker-large",
                "embedding_model": "all-MiniLM-L6-v2",
                "llm": "gemini",
                "chunk_size": 512,
                "top_k": 8
            }
        )
        return {
            "answer": answer,
            "rewritten_query": rewritten_query,
            "contexts": contexts,
            "ragas": ragas_results,
            "critique": critique
        }