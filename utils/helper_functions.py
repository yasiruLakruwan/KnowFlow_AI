from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from exeption import CustomExeption
from logger import get_logger
from langchain_chroma import Chroma
from config.path_config import presist_dir,document_pkl
from utils.embeding_model import embeding_model,gemini_model
import os
import pickle
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import (context_precision,faithfulness,answer_relevancy)
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage,SystemMessage,AIMessage

logger = get_logger(__name__)    

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

def load_vector_store():
    try:    
        logger.info("Loading existing vector database......")
        embed_model = embeding_model()

        db = Chroma(
            persist_directory=presist_dir,
            embedding_function=embed_model
        )
        logger.info("db loaded successfully....")

        return db
    
    except Exception as e:
        raise CustomExeption("Error loading the vector db",e)
    
def load_documets_for_bm25(document_pkl:str):
    try:
        file_path = os.path.join(document_pkl,"all_documents.pkl")
        if not os.path.exists(file_path):
            raise CustomExeption(f"File path {file_path} doesnot exists")
        with open(file_path,"rb") as f:
            documents = pickle.load(f)
        return documents
    
    except Exception as e:
        raise CustomExeption("Error hapening in load document.pkl file")


# Build ragas dataset
# RAGAS requires references column for validation

def build_ragas_dataset(user_inputs,responses,retrieved_contexts,references=None):
    
    if references is None:
        references = [""] * len(user_inputs)
    
    data ={
        "user_input":user_inputs,
        "response":responses,
        "retrieved_contexts":retrieved_contexts,
        "reference":references
    }

    return Dataset.from_dict(data)

# create history aware retriever

def history_aware_retriever():
    contextualize_prompt = ChatPromptTemplate.from_messages([
        ("system",
        "Given the chat history and the latest user question, "
        "rewrite the question so it can be understood without the chat history. "
        "Do NOT answer the question."),
        ("human", "Chat history:\n{chat_history}\n\nQuestion:\n{input}")
    ])

    llm = gemini_model()

    history_aware_retriever = (
        {
            "input":RunnablePassthrough(),
            "chat_history": RunnablePassthrough(),
        }
        | contextualize_prompt
        | llm
        | RunnableLambda(extract)
    )


# Run RAGAS evaluation
def run_ragas(dataset,model):

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    model = gemini_model()
    results = evaluate(
        dataset,
        metrics=[
            context_precision,
            faithfulness,
            answer_relevancy
        ],
        llm = model,
        embeddings=embeddings
    )
    return results






if __name__== "__main__":
    db = load_vector_store()
    print(db) 
    documents = load_documets_for_bm25(document_pkl)
    print(len(documents)) 




