#!/usr/bin/env python3
"""
Test and create Cohere embedding vectorstore
"""

import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from dotenv import load_dotenv
from rag import CustomAzureEmbeddings, RAGFrontend

# Load environment
load_dotenv()

def test_cohere_embedding():
    """Test Cohere embedding model"""
    print("=== Testing Cohere Embedding Model ===")
    
    try:
        model_name = "Cohere-embed-v3-multilingual"
        print(f"Testing {model_name}...")
        
        # Test basic embedding functionality
        embedding_model = CustomAzureEmbeddings(model_name)
        print("✅ Cohere embedding model created successfully")
        
        # Test single query embedding
        test_text = "This is a test sentence for embedding."
        result = embedding_model.embed_query(test_text)
        print(f"✅ Single embedding successful, dimension: {len(result)}")
        
        # Test batch embedding
        test_texts = ["First test sentence", "Second test sentence"]
        batch_result = embedding_model.embed_documents(test_texts)
        print(f"✅ Batch embedding successful, {len(batch_result)} embeddings created")
        
        return True
        
    except Exception as e:
        print(f"❌ Cohere embedding test failed: {e}")
        return False

def create_cohere_vectorstore():
    """Create Cohere vectorstore from JSON data"""
    print("\n=== Creating Cohere Vectorstore ===")
    
    try:
        # Check if JSON file exists
        json_file = "authors_with_h_index.json"
        if not os.path.exists(json_file):
            print(f"❌ JSON file {json_file} not found")
            return False
        
        print(f"✅ Found JSON file: {json_file}")
        
        # Create RAG frontend with Cohere embedding
        model_name = "Cohere-embed-v3-multilingual"
        rag_frontend = RAGFrontend(
            embedding_model=model_name,
            json_file_path=json_file
        )
        
        print(f"Creating vectorstore with {model_name}...")
        vectorstore = rag_frontend.create_vector_store()
        
        if vectorstore:
            # Save the vectorstore
            save_path = "Cohere_embed_v3_multilingual_faiss_index"
            vectorstore.save_local(save_path)
            print(f"✅ Vectorstore saved to {save_path}")
            return True
        else:
            print("❌ Vectorstore creation failed")
            return False
            
    except Exception as e:
        print(f"❌ Vectorstore creation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_vectorstore_loading():
    """Test loading the created vectorstore"""
    print("\n=== Testing Vectorstore Loading ===")
    
    try:
        from langchain_community.vectorstores import FAISS
        
        model_name = "Cohere-embed-v3-multilingual"
        save_path = "Cohere_embed_v3_multilingual_faiss_index"
        
        if not os.path.exists(save_path):
            print(f"❌ Vectorstore folder {save_path} does not exist")
            return False
        
        # Test loading
        embedding_model = CustomAzureEmbeddings(model_name)
        vectorstore = FAISS.load_local(
            save_path,
            embeddings=embedding_model,
            allow_dangerous_deserialization=True
        )
        
        # Test retrieval
        retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
        test_query = "computer science professor"
        results = retriever.get_relevant_documents(test_query)
        
        print(f"✅ Vectorstore loaded successfully")
        print(f"✅ Retrieved {len(results)} documents for test query")
        print(f"Sample result: {results[0].page_content[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Vectorstore loading test failed: {e}")
        return False

if __name__ == "__main__":
    print("Cohere Embedding Vectorstore Test")
    print("=" * 40)
    
    # Test 1: Basic Cohere embedding functionality
    if not test_cohere_embedding():
        print("❌ Basic embedding test failed, stopping...")
        exit(1)
    
    # Test 2: Create vectorstore
    if not create_cohere_vectorstore():
        print("❌ Vectorstore creation failed, stopping...")
        exit(1)
    
    # Test 3: Test loading the vectorstore
    test_vectorstore_loading()
    
    print("\n" + "=" * 40)
    print("Test complete!")
