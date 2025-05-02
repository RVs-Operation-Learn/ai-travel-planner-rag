from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings

embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db = Chroma(persist_directory="./vectorstore", embedding_function=embedding_model)

def retrieve_travel_info(query, city):
    # Filter by metadata city
    return db.similarity_search(query, k=3, filter={"city": city})
