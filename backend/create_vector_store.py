from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
import json
import os

# Load knowledge base
with open("./data/knowledge_base.json", "r", encoding="utf-8") as f:
    knowledge_data = json.load(f)

# Initialize embedding model
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Split and tag data
text_splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=30)
docs = []

for item in knowledge_data:
    chunks = text_splitter.split_text(item["info"])
    for chunk in chunks:
        doc = Document(page_content=chunk, metadata={"city": item["city"]})
        docs.append(doc)

# Save to Chroma DB
if os.path.exists("./vectorstore"):
    import shutil
    shutil.rmtree("./vectorstore")

db = Chroma.from_documents(docs, embedding_model, persist_directory="./vectorstore")
db.persist()
print("✅ Vector store created and persisted.")