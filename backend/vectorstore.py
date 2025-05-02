from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Set up embeddings
embedding = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))

# Use LangChain's Chroma wrapper, specify persist_directory (optional)
vectorstore = Chroma(
    collection_name="travel_data",
    embedding_function=embedding,
    persist_directory="./chroma_db"
)
