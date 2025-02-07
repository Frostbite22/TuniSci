import streamlit as st
import pandas as pd
import json
import time
from rag import AzureAIChat, CustomAzureEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
import os
from dotenv import load_dotenv
from pathlib import Path

# Load from .env if exists
load_dotenv()

# Load from .streamlit/secrets.toml for Streamlit deployment
if Path(".streamlit/secrets.toml").exists():
    os.environ["GITHUB_TOKEN"] = st.secrets["GITHUB_TOKEN"]

# Initialize session state for chat history and user input
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'user_input' not in st.session_state:
    st.session_state.user_input = ""

# Function to handle sending messages
def send_message():
    if st.session_state.user_input:
        user_query = st.session_state.user_input
        retriever = st.session_state.get('retriever')
        
        if retriever:
            response, model_used = query_chat_model(user_query, retriever)
            if response:
                st.session_state.chat_history.append({"user": user_query, "bot": response})
                # Clear the input after sending
                st.session_state.user_input = ""
            else:
                st.error("All models failed. Please try again later.")


# Embedding models and corresponding FAISS index folders
EMBEDDING_MODELS = {
    "Cohere-embed-v3-english": "cohere_english_faiss_index",
    "text-embedding-3-small": "openai_small_faiss_index",
    "text-embedding-3-large": "openai_large_faiss_index",
}

# Chat models for dynamic switching
CHAT_MODELS = [
    "Cohere-command-r-plus-08-2024",
    "Cohere-command-r-plus",
    "Cohere-command-r-08-2024",
    "gpt-4o",
    "gpt-4o-mini"
]

# Load embedding and vector store with dynamic switching
@st.cache_resource
def load_rag_components():
    for embedding_model_name, index_folder in EMBEDDING_MODELS.items():
        try:
            if "Cohere" in embedding_model_name:
                embedding_model = CustomAzureEmbeddings(embedding_model_name)
            else:
                from langchain.embeddings import OpenAIEmbeddings
                embedding_model = OpenAIEmbeddings(model=embedding_model_name)

            vectorstore = FAISS.load_local(
                index_folder,
                embeddings=embedding_model,
                allow_dangerous_deserialization=True
            )
            retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
            return retriever, embedding_model_name
        except Exception as e:
            st.warning(f"Failed to load {embedding_model_name} with index {index_folder}. Error: {e}")
            time.sleep(1)
    return None, None

# Function to query the chat model with error handling and dynamic switching
def query_chat_model(user_query, retriever):
    for model_name in CHAT_MODELS:
        try:
            st.write(f"Trying chat model: {model_name}")
            chat_model = AzureAIChat(chat_model=model_name)
            qa_chain = RetrievalQA.from_chain_type(llm=chat_model(), retriever=retriever)
            response = qa_chain.invoke(user_query)
            return response["result"], model_name
        except Exception as e:
            if "rate limit" in str(e).lower():
                st.warning(f"Model {model_name} hit the rate limit. Switching to the next model.")
            elif "unauthorized" in str(e).lower():
                st.warning(f"Model {model_name} returned an authorization error. Switching to the next model.")
            elif "timeout" in str(e).lower():
                st.warning(f"Model {model_name} timed out. Switching to the next model.")
            else:
                st.error(f"Unexpected error with {model_name}: {e}")
            time.sleep(1)
    return None, None

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

def main():
    st.title("TuniSci")

    # Tabs for different views
    tab1, tab2 = st.tabs(["Author Table", "Chat"])

    with tab1:
        st.header("Authors H-Index Table")
        df = load_authors_data()
        st.write(f"Average H-Index: {df['hindex'].astype(int).mean():.2f}")
        st.dataframe(df.head(1000))

    with tab2:
        st.header("Chat")
        retriever, embedding_model_used = load_rag_components()
        
        if not retriever:
            st.error("Failed to load any embedding model. Please try again later.")
            return
        
        # Store retriever in session state for access in callback
        st.session_state['retriever'] = retriever
        st.write(f"Using embedding model: {embedding_model_used}")

        # Chat input with callback
        st.text_input(
            "Ask a question about authors:",
            key="user_input",
            on_change=send_message,
            value=st.session_state.user_input
        )

        # Display chat history
        st.subheader("Chat History")
        for chat in st.session_state.chat_history:
            st.markdown(f"**You:** {chat['user']}")
            st.markdown(f"**Bot:** {chat['bot']}")
            st.markdown("---")

        # Clear chat history button
        if st.button("Clear Chat History"):
            st.session_state.chat_history = []
            st.session_state.user_input = ""

if __name__ == "__main__":
    main()
