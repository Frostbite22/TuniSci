### Intference using the RAG model
# get the embedding model
from rag import AzureAIChat, CustomAzureEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_openai import OpenAIEmbeddings


embedding_model = CustomAzureEmbeddings("Cohere-embed-v3-english")
# embedding_model = OpenAIEmbeddings(model="text-embedding-3-large")

# Load the FAISS index
vectorstore = FAISS.load_local(
    "cohere_faiss_index", 
    embeddings=embedding_model,
    allow_dangerous_deserialization=True
)
retriever = vectorstore.as_retriever(search_kwargs={"k": 10})
# get the chat model
chat_model = AzureAIChat(chat_model="Cohere-command-r-plus-08-2024")
# Create a QA chain using the retriever
qa_chain = RetrievalQA.from_chain_type(llm=chat_model(), retriever=retriever)

query = "Who is Adel Trabelsi?"

response = qa_chain.invoke(query)
print(response["query"])
print(response["result"])
