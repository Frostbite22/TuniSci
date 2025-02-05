### Creating the embeddings,  vector store and saving the FAISS index
from rag import RAGFrontend


rag = RAGFrontend(embedding_model="Cohere-embed-v3-english",json_file_path="authors_with_h_index.json")  
vectorstore = rag.create_vector_store()
# Save the FAISS index
vectorstore.save_local("cohere_faiss_index")

print("FAISS index saved successfully")

