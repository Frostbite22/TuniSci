### Intference using the RAG model
# get the embedding model
from rag import AzureAIChat, CustomAzureEmbeddings, SentenceTransformerWrapper
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_openai import OpenAIEmbeddings

chat_model = AzureAIChat(chat_model="Cohere-command-r-plus-08-2024")

from langchain.retrievers import ContextualCompressionRetriever
# from langchain.retrievers.document_compressors import LengthBasedExampleSelector
from langchain.memory import ConversationTokenBufferMemory

# Load embeddings and vectorstore as before
# embedding_model = CustomAzureEmbeddings(model_name="Cohere-embed-v3-english")
# embedding_model = OpenAIEmbeddings(model="text-embedding-3-large")
embedding_model = SentenceTransformerWrapper(model="sentence-transformers/paraphrase-MiniLM-L6-v2")
vectorstore = FAISS.load_local(
    "Paraphrase_MiniLM_L6_v2_faiss_index", 
    embeddings=embedding_model,
    allow_dangerous_deserialization=True
)

# Create a retriever with reduced k and max_token limits
retriever = vectorstore.as_retriever(
    search_kwargs={
        "k": 5,  # Reduced from 10 to 5
        "fetch_k": 8,  # Fetch more candidates initially
        "maximal_marginal_relevance": False,  # Use MMR for diversity
    }
)

# Create memory with token limit
memory = ConversationTokenBufferMemory(
    llm=chat_model(),
    max_token_limit=6000  # Leave room for response
)

# Create QA chain with specific prompt template to control context length
from langchain.prompts import PromptTemplate

prompt_template = """Answer the question based on the following context. Keep your response focused and concise.

Context: {context}

Question: {question}

Answer:"""

PROMPT = PromptTemplate(
    template=prompt_template, 
    input_variables=["context", "question"]
)

# Create the QA chain with the custom prompt
qa_chain = RetrievalQA.from_chain_type(
    llm=chat_model(),
    chain_type="stuff",
    retriever=retriever,
    chain_type_kwargs={
        "prompt": PROMPT,
        "verbose": True
    },
    return_source_documents=True,  # Optional: to see what documents were used
)

# Query function with error handling
def query_qa_chain(query):
    try:
        response = qa_chain.invoke(query)
        print("Query:", response["query"])
        print("\nAnswer:", response["result"])
        
        # Optionally print sources
        if "source_documents" in response:
            print("\nSources used:")
            for doc in response["source_documents"]:
                print(f"- {doc.metadata.get('source', 'Unknown source')}")
                
    except Exception as e:
        print(f"Error during query: {str(e)}")
        print("Try reducing the context window or simplifying the query.")

# Test the query
query = "Who is the most successful professor in hindex score in nuclear physics?"
query_qa_chain(query)