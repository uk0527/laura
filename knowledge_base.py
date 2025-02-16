import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Load embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
vector_dim = 384  # Dimension of embeddings
faiss_index = faiss.IndexFlatL2(vector_dim)
knowledge_store = []

def add_knowledge_entry(text):
    """Adds a new knowledge entry to FAISS"""
    embedding = embedding_model.encode([text])[0]
    knowledge_store.append(text)
    faiss_index.add(np.array([embedding], dtype=np.float32))

def retrieve_knowledge(query):
    """Retrieves relevant knowledge based on a query"""
    if not knowledge_store:
        return "No relevant knowledge found."

    query_embedding = embedding_model.encode([query])[0]
    distances, closest_doc_index = faiss_index.search(np.array([query_embedding], dtype=np.float32), k=1)

    # Ensure valid index exists before accessing
    if len(closest_doc_index) == 0 or closest_doc_index[0][0] >= len(knowledge_store):
        return "No relevant knowledge found."

    return knowledge_store[closest_doc_index[0][0]]
