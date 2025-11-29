from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()

def embeding_model():
    embedding_model = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2"
            )
    return embedding_model

def gemini_model():
    model = ChatGoogleGenerativeAI(
        google_api_key=os.getenv("GEMINI_API_KEY"), # Required by library, any string works
        model="gemini-2.5-flash" # The name of the model you pulled with Ollama
    )
    return model


