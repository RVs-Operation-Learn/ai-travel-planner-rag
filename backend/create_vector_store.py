import json
import chromadb
from sentence_transformers import SentenceTransformer

# Initialize ChromaDB client
chroma_client = chromadb.PersistentClient(path="./chroma_db")

# Create or get collection
collection = chroma_client.get_or_create_collection(name="travel_info")

# Load knowledge base
with open("./data/knowledge_base.json", "r", encoding="utf-8") as f:
    knowledge_base = json.load(f)

# Load embedding model (local HuggingFace model)
embedder = SentenceTransformer('all-MiniLM-L6-v2')

# Prepare data for insertion
documents = []
ids = []
metadatas = []

for idx, item in enumerate(knowledge_base):
    city = item["city"]
    info = item["info"]
    embedding = embedder.encode(info).tolist()
    
    documents.append(info)
    ids.append(str(idx))  # IDs must be strings
    metadatas.append({"city": city})

# Insert into ChromaDB
collection.add(
    documents=documents,
    embeddings=[embedder.encode(doc).tolist() for doc in documents],
    metadatas=metadatas,
    ids=ids
)

# Save to disk
# chroma_client.persist()

print("✅ Vector store created and saved!")