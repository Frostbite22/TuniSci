#!/usr/bin/env python3
"""
Test the streamlit app functionality without running the full streamlit server
"""

import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from dotenv import load_dotenv

# Load environment
load_dotenv()

def test_embedding_loading():
    """Test if embedding models load correctly"""
    print("=== Testing Embedding Model Loading ===")
    
    from rag import CustomAzureEmbeddings
    from langchain_community.vectorstores import FAISS
    
    # Test the sentence transformer embedding first
    embedding_model_name = "sentence-transformers/paraphrase-MiniLM-L6-v2"
    index_folder = "Paraphrase_MiniLM_L6_v2_faiss_index"
    
    try:
        print(f"Testing {embedding_model_name}...")
        
        # Check if the index folder exists
        if not os.path.exists(index_folder):
            print(f"❌ Index folder {index_folder} not found")
            return False
        
        # Try to load the embedding model
        from rag import SentenceTransformerWrapper
        embedding_model = SentenceTransformerWrapper(model=embedding_model_name)
        print(f"✅ Embedding model loaded successfully")
        
        # Try to load the vector store
        vectorstore = FAISS.load_local(
            index_folder,
            embeddings=embedding_model,
            allow_dangerous_deserialization=True
        )
        print(f"✅ Vector store loaded successfully")
        
        # Create retriever
        retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
        print(f"✅ Retriever created successfully")
        
        return retriever
        
    except Exception as e:
        print(f"❌ Failed to load embedding components: {e}")
        return None

def test_chat_integration():
    """Test the full chat integration"""
    print("\n=== Testing Chat Integration ===")
    
    from rag import AzureAIChat
    from langchain.chains import RetrievalQA
    
    # First load the retriever
    retriever = test_embedding_loading()
    if not retriever:
        print("❌ Cannot test chat integration without retriever")
        return False
    
    # Test models
    test_models = ["gpt-4o-mini", "Cohere-command-r-plus-08-2024"]
    
    for model in test_models:
        print(f"\n--- Testing chat model: {model} ---")
        try:
            # Create chat model
            chat_model = AzureAIChat(chat_model=model)
            llm = chat_model()
            print(f"✅ Chat model {model} created successfully")
            
            # Create QA chain
            qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
            print(f"✅ QA chain created successfully")
            
            # Test with a simple query
            test_query = "Who is a professor in computer science?"
            response = qa_chain.invoke(test_query)
            print(f"✅ Query successful")
            print(f"Response preview: {str(response['result'])[:100]}...")
            
            return True
            
        except Exception as e:
            print(f"❌ Failed with model {model}: {e}")
            continue
    
    return False

def test_streamlit_functions():
    """Test streamlit app functions directly"""
    print("\n=== Testing Streamlit Functions ===")
    
    try:
        # Import without running streamlit
        import streamlit_app
        
        # Test load_rag_components function
        print("Testing load_rag_components...")
        
        # Mock streamlit error function
        class MockStreamlit:
            @staticmethod
            def error(msg):
                print(f"ST ERROR: {msg}")
        
        # Temporarily replace st with mock
        original_st = streamlit_app.st
        streamlit_app.st = MockStreamlit()
        
        try:
            retriever = streamlit_app.load_rag_components("sentence-transformers/paraphrase-MiniLM-L6-v2")
            if retriever:
                print("✅ load_rag_components works")
            else:
                print("❌ load_rag_components returned None")
        finally:
            # Restore original st
            streamlit_app.st = original_st
        
        return True
        
    except Exception as e:
        print(f"❌ Streamlit function test failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing Streamlit App Components")
    print("=" * 40)
    
    # Test embedding loading
    test_embedding_loading()
    
    # Test chat integration
    test_chat_integration()
    
    # Test streamlit functions
    test_streamlit_functions()
    
    print("\n" + "=" * 40)
    print("Test complete!")
