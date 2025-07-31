#!/usr/bin/env python3
"""
Debug script to test Azure AI Studio API connection
"""

import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from azure.ai.inference import EmbeddingsClient
from azure.core.credentials import AzureKeyCredential

# Load environment variables
load_dotenv()

ENDPOINT = "https://models.inference.ai.azure.com"

def test_azure_chat_models():
    """Test Azure Chat models"""
    print("=== Testing Azure Chat Models ===")
    
    # Get the token
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("❌ ERROR: GITHUB_TOKEN not found in environment variables")
        return
    
    print(f"✅ Found GITHUB_TOKEN (length: {len(token)})")
    
    # Test models to try
    test_models = [
        "gpt-4o",
        "gpt-4o-mini",
        "Cohere-command-r-plus-08-2024",
        "Cohere-command-r-plus",
    ]
    
    for model in test_models:
        print(f"\n--- Testing model: {model} ---")
        try:
            # Create the Azure OpenAI client
            llm = AzureChatOpenAI(
                azure_endpoint=ENDPOINT,
                api_key=token,
                api_version="2024-03-01-preview",  # Try this version first
                deployment_name=model,
                temperature=0.1,
                max_tokens=100
            )
            
            # Test with a simple prompt
            response = llm.invoke("Hello, say 'test successful' in one sentence.")
            print(f"✅ SUCCESS: {model}")
            print(f"Response: {response.content}")
            
        except Exception as e:
            print(f"❌ FAILED: {model}")
            print(f"Error: {str(e)}")
            print(f"Error type: {type(e).__name__}")

def test_azure_embedding_models():
    """Test Azure Embedding models"""
    print("\n\n=== Testing Azure Embedding Models ===")
    
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("❌ ERROR: GITHUB_TOKEN not found")
        return
    
    test_models = [
        "Cohere-embed-v3-multilingual",
        "Cohere-embed-v3-english"
    ]
    
    for model in test_models:
        print(f"\n--- Testing embedding model: {model} ---")
        try:
            client = EmbeddingsClient(
                endpoint=ENDPOINT,
                credential=AzureKeyCredential(token)
            )
            
            # Test with simple text
            response = client.embed(input=["test text"], model=model)
            embeddings = [item.embedding for item in response.embeddings]
            print(f"✅ SUCCESS: {model}")
            print(f"Embedding dimension: {len(embeddings[0])}")
            
        except Exception as e:
            print(f"❌ FAILED: {model}")
            print(f"Error: {str(e)}")
            print(f"Error type: {type(e).__name__}")

def test_different_api_versions():
    """Test different API versions for chat models"""
    print("\n\n=== Testing Different API Versions ===")
    
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("❌ ERROR: GITHUB_TOKEN not found")
        return
    
    api_versions = [
        "2024-03-01-preview",
        "2024-07-01-preview", 
        "2024-02-01",
        "2023-12-01-preview",
        "2023-07-01-preview"
    ]
    
    model = "gpt-4o-mini"  # Use a reliable model for testing
    
    for api_version in api_versions:
        print(f"\n--- Testing API version: {api_version} ---")
        try:
            llm = AzureChatOpenAI(
                azure_endpoint=ENDPOINT,
                api_key=token,
                api_version=api_version,
                deployment_name=model,
                temperature=0.1,
                max_tokens=50
            )
            
            response = llm.invoke("Say hello")
            print(f"✅ SUCCESS: API version {api_version}")
            print(f"Response: {response.content}")
            break  # If successful, stop testing other versions
            
        except Exception as e:
            print(f"❌ FAILED: API version {api_version}")
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    print("Azure AI Studio API Diagnostic Tool")
    print("=" * 40)
    
    # Test chat models
    test_azure_chat_models()
    
    # Test embedding models
    test_azure_embedding_models()
    
    # Test different API versions
    test_different_api_versions()
    
    print("\n" + "=" * 40)
    print("Diagnostic complete!")
