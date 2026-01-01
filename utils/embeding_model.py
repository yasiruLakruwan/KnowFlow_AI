from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()

# Free embedding model........
def embeding_model():
    embedding_model = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2",
                model_kwargs = {"device":"cpu"},
                encode_kwargs = {"normalize_embeddings":True}
            )
    return embedding_model

# Free gemini model...........
def gemini_model():
    gemini_model = ChatGoogleGenerativeAI(
        google_api_key=os.getenv("GEMINI_API_KEY"), # Required by library, any string works
        model="gemini-2.0-flash-lite" # The name of the model you pulled with Ollama
    )
    return gemini_model