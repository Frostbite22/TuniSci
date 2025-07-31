#!/usr/bin/env python3
"""
Test the updated Azure integration
"""

import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from dotenv import load_dotenv
from rag import AzureAIChat, CustomAzureEmbeddings

# Load environment variables
load_dotenv()

def test_updated_azure_chat():
    """Test the updated Azure chat implementation"""
    print("=== Testing Updated Azure Chat Integration ===")
    
    test_models = [
        "gpt-4o-mini",
        "Cohere-command-r-plus-08-2024"
    ]
    
    for model in test_models:
        print(f"\n--- Testing model: {model} ---")
        try:
            chat = AzureAIChat(chat_model=model)
            llm = chat()
            
            # Test with a simple prompt
            response = llm.invoke("Hello, say 'test successful' in one sentence.")
            print(f"✅ SUCCESS: {model}")
            print(f"Response: {response}")  # LLM returns string directly, not .content
            
        except Exception as e:
            print(f"❌ FAILED: {model}")
            print(f"Error: {str(e)}")
            print(f"Error type: {type(e).__name__}")

def test_updated_azure_embeddings():
    """Test the updated Azure embeddings implementation"""
    print("\n\n=== Testing Updated Azure Embeddings Integration ===")
    
    test_models = [
        "Cohere-embed-v3-multilingual",
        "Cohere-embed-v3-english"
    ]
    
    for model in test_models:
        print(f"\n--- Testing embedding model: {model} ---")
        try:
            embeddings = CustomAzureEmbeddings(model_name=model)
            
            # Test single query
            result = embeddings.embed_query("test text")
            print(f"✅ SUCCESS: {model}")
            print(f"Embedding dimension: {len(result)}")
            
            # Test batch embedding
            batch_result = embeddings.embed_documents(["test text 1", "test text 2"])
            print(f"Batch embedding result: {len(batch_result)} embeddings")
            
        except Exception as e:
            print(f"❌ FAILED: {model}")
            print(f"Error: {str(e)}")
            print(f"Error type: {type(e).__name__}")

if __name__ == "__main__":
    print("Testing Updated Azure AI Integration")
    print("=" * 40)
    
    # Test chat models
    test_updated_azure_chat()
    
    # Test embedding models
    test_updated_azure_embeddings()
    
    print("\n" + "=" * 40)
    print("Test complete!")
