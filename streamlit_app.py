import streamlit as st
import pandas as pd
import json

# Import RAG dependencies
from rag import AzureAIChat, CustomAzureEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA

# Initialize session state for chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Load embedding and vector store
@st.cache_resource
def load_rag_components():
    embedding_model = CustomAzureEmbeddings("Cohere-embed-v3-english")
    vectorstore = FAISS.load_local(
        "cohere_faiss_index", 
        embeddings=embedding_model,
        allow_dangerous_deserialization=True
    )
    retriever = vectorstore.as_retriever(search_kwargs={"k": 10})
    chat_model = AzureAIChat(chat_model="Cohere-command-r-plus-08-2024")
    qa_chain = RetrievalQA.from_chain_type(llm=chat_model(), retriever=retriever)
    return qa_chain

# Load authors data
@st.cache_data
def load_authors_data():
    with open("authors_with_h_index.json", "r") as file:
        authors_h_index = json.load(file)

    authors_json = [
        {
            "profile_name": author.get("profile_name", "N/A"),
            "profile_affiliations": author.get("profile_affiliations", "N/A"),
            "profile_interests": author.get("profile_interests", "N/A"),
            "hindex": author.get("hindex", 0),
            "i10index": author.get("i10index", 0)
        }
        for author in authors_h_index
    ]

    sorted_authors = sorted(
        authors_json,
        key=lambda x: (int(x["hindex"]), int(x["i10index"])),
        reverse=True
    )

    for i, author in enumerate(sorted_authors):
        author["rank"] = i + 1

    return pd.DataFrame(sorted_authors)

# Main Streamlit app
def main():
    st.title("Authors Explorer with RAG")

    # Tabs for different views
    tab1, tab2 = st.tabs(["Author Table", "RAG Chat"])

    with tab1:
        st.header("Authors H-Index Table")
        df = load_authors_data()
        st.write(f"Average H-Index: {df['hindex'].astype(int).mean():.2f}")
        st.dataframe(df.head(1000))

    with tab2:
        st.header("RAG Chat")
        
        # Initialize QA chain
        qa_chain = load_rag_components()

        # Chat input
        user_query = st.text_input("Ask a question about authors:", key="query_input")
        
        # Send button
        if st.button("Send"):
            if user_query:
                # Perform RAG query
                try:
                    response = qa_chain.invoke(user_query)
                    
                    # Update chat history
                    st.session_state.chat_history.append({
                        "user": user_query, 
                        "bot": response["result"]
                    })
                except Exception as e:
                    st.error(f"An error occurred: {e}")

        # Display chat history
        st.subheader("Chat History")
        for chat in st.session_state.chat_history:
            st.markdown(f"**You:** {chat['user']}")
            st.markdown(f"**Bot:** {chat['bot']}")
            st.markdown("---")

        # Clear chat history button
        if st.button("Clear Chat History"):
            st.session_state.chat_history = []

if __name__ == "__main__":
    main()