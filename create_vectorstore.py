### Creating the embeddings,  vector store and saving the FAISS index
from rag import RAGFrontend

# Cohere-embed-v3-english
# Cohere-embed-v3-multilingual
# text-embedding-3-large
# text-embedding-3-small
# rag = RAGFrontend(embedding_model="Cohere-embed-v3-english",json_file_path="authors_with_h_index.json")  

# For SentenceTransformer embeddings
rag = RAGFrontend(
    embedding_model="sentence-transformers/paraphrase-MiniLM-L6-v2",
    json_file_path="authors_with_h_index.json"
)
vectorstore = rag.create_vector_store()
# Save the FAISS index
vectorstore.save_local("Paraphrase_MiniLM_L6_v2_faiss_index")

print("FAISS index saved successfully")

