import openai
import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain_community.llms import OpenAI
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.agents import initialize_agent, Tool, AgentType

# Load environment variables
load_dotenv()

# Ensure you have the OpenAI API key in your environment variables
api_key = os.getenv("OPENAI_API_KEY")  # Correct API key initialization

# Initialize the OpenAI model using langchain
llm = OpenAI(model_name="gpt-3.5-turbo", openai_api_key=api_key)  # Use the correct model parameter

# Make sure `vectorstore` is set up and accessible
from vectorstore import vectorstore  # Assuming vectorstore is set up

# Use the vector store as a retriever
retriever = vectorstore.as_retriever()
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db = Chroma(persist_directory="./vectorstore", embedding_function=embedding_model)

# You can initialize tools here if needed for agents
tools = [
    Tool(
        name="Search",
        func=db.similarity_search,
        description="Retrieve information from the knowledge base"
    )
]

# Initialize the agent
agent = initialize_agent(tools, llm, agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

# Chat function
def generate_answer(query: str, city: str) -> str:
    full_query = f"{query} about {city}"
    response = agent.run(full_query)
    return response
