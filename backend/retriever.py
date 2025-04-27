import chromadb
from sentence_transformers import SentenceTransformer

# Initialize client
chroma_client = chromadb.PersistentClient(path="./chroma_db")

# Load embedding model
embedder = SentenceTransformer('all-MiniLM-L6-v2')

# Get collection
collection = chroma_client.get_or_create_collection(name="travel_info")

def retrieve_travel_info(query: str, top_k: int = 5, city: str = None):
    """
    Given a user query, retrieve top_k relevant travel information,
    optionally filter by city.
    """
    # Embed the query
    query_embedding = embedder.encode(query).tolist()

    # Query ChromaDB
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas"]
    )

    documents = results["documents"][0] if results["documents"] else []

    # Optional: filter by city keyword
    if city:
        documents = [doc for doc in documents if city.lower() in doc.lower()]

    return documents