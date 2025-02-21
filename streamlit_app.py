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
from rag import SentenceTransformerWrapper, OpenAIEmbeddings

# Load from .env if exists
load_dotenv()

# Load from .streamlit/secrets.toml for Streamlit deployment
if Path(".streamlit/secrets.toml").exists():
    os.environ["GITHUB_TOKEN"] = st.secrets["GITHUB_TOKEN"]

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'selected_embedding_model' not in st.session_state:
    st.session_state.selected_embedding_model = "Cohere-embed-v3-english"
if 'selected_chat_model' not in st.session_state:
    st.session_state.selected_chat_model = "Cohere-command-r-plus-08-2024"

# Embedding models and corresponding FAISS index folders
EMBEDDING_MODELS = {
    "Cohere-embed-v3-english": "cohere_english_faiss_index_v2",
    "Cohere-embed-v3-multilingual": "Cohere_embed_v3_multilingual_faiss_index",
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2": "paraphrase_multilingual_faiss_index",
    "sentence-transformers/all-MiniLM-L6-v2": "allMiniLM_L6_v2_faiss_index",
    "sentence-transformers/paraphrase-MiniLM-L6-v2": "Paraphrase_MiniLM_L6_v2_faiss_index"
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
@st.cache_resource(show_spinner=False)
def load_rag_components(embedding_model_name):
    try:
        index_folder = EMBEDDING_MODELS[embedding_model_name]
        if "Cohere" in embedding_model_name:
            embedding_model = CustomAzureEmbeddings(embedding_model_name)
        else:
            embedding_model = SentenceTransformerWrapper(model=embedding_model_name)

        vectorstore = FAISS.load_local(
            index_folder,
            embeddings=embedding_model,
            allow_dangerous_deserialization=True
        )
        retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
        return retriever
    except Exception as e:
        st.error(f"Failed to load {embedding_model_name}. Error: {e}")
        return None

# Function to query the chat model with the selected model
def query_chat_model(user_query, retriever, selected_chat_model):
    try:
        chat_model = AzureAIChat(chat_model=selected_chat_model)
        qa_chain = RetrievalQA.from_chain_type(llm=chat_model(), retriever=retriever)
        response = qa_chain.invoke(user_query)
        return response["result"], selected_chat_model
    except Exception as e:
        error_message = str(e).lower()
        if "rate limit" in error_message:
            st.warning(f"Model {selected_chat_model} hit the rate limit.")
        elif "unauthorized" in error_message:
            st.warning(f"Model {selected_chat_model} returned an authorization error.")
        elif "timeout" in error_message:
            st.warning(f"Model {selected_chat_model} timed out.")
        else:
            st.error(f"Unexpected error with {selected_chat_model}: {e}")
        return None, None

# Function to process the message
def process_message(user_query, retriever, selected_chat_model):
    if user_query and retriever:
        response, model_used = query_chat_model(user_query, retriever, selected_chat_model)
        if response:
            st.session_state.chat_history.insert(0, {"user": user_query, "bot": response})
            return True
        else:
            st.error("Failed to get response. Please try again or select a different model.")
    return False

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
    return pd.DataFrame(sorted_authors).set_index("rank")

def main():
    st.title("TuniSci")

    # Tabs for different views
    tab1, tab2 = st.tabs(["Author Table", "Chat"])

    with tab1:
        st.header("Authors H-Index Table in Tunisia")
        df = load_authors_data()
        st.write(f"Average H-Index: {df['hindex'].astype(int).mean():.2f}")
        st.dataframe(df.head(1000))

    with tab2:
        st.header("Chat")
        
        # Model selection dropdowns in side-by-side columns
        col1, col2 = st.columns(2)
        
        with col1:
            selected_embedding = st.selectbox(
                "Select Embedding Model",
                options=list(EMBEDDING_MODELS.keys()),
                index=list(EMBEDDING_MODELS.keys()).index(st.session_state.selected_embedding_model)
            )
            
        with col2:
            selected_chat = st.selectbox(
                "Select Chat Model",
                options=CHAT_MODELS,
                index=CHAT_MODELS.index(st.session_state.selected_chat_model)
            )
        
        # Update session state if selection changed
        if selected_embedding != st.session_state.selected_embedding_model:
            st.session_state.selected_embedding_model = selected_embedding
            st.rerun()
            
        st.session_state.selected_chat_model = selected_chat
        
        # Load retriever with selected embedding model
        retriever = load_rag_components(selected_embedding)
        
        if not retriever:
            st.error("Failed to load embedding model. Please try a different model.")
            return

        # Chat interface
        st.write("Ask a question about authors:")
        
        # Input and button layout
        col1, col2 = st.columns([5, 1])
        
        with col1:
            user_input = st.text_input("", key="query_input", label_visibility="collapsed")
        
        with col2:
            send_pressed = st.button("Send", type="primary", use_container_width=True)

        # Process message when send is pressed
        if send_pressed and user_input:
            process_message(user_input, retriever, selected_chat)

        # Display chat history
        if st.session_state.chat_history:
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