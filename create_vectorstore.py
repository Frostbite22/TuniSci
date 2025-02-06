### Creating the embeddings,  vector store and saving the FAISS index
from rag import RAGFrontend


rag = RAGFrontend(embedding_model="text-embedding-3-small",json_file_path="authors_with_h_index.json")  
vectorstore = rag.create_vector_store()
# Save the FAISS index
vectorstore.save_local("openai_small_faiss_index")

print("FAISS index saved successfully")

