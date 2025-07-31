#!/usr/bin/env python3
"""
Test script to debug Azure AI Studio API connection issues
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

def test_github_token():
    """Test if GitHub token is properly loaded"""
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("❌ GITHUB_TOKEN not found in environment variables")
        return False
    else:
        print(f"✅ GITHUB_TOKEN found: {token[:10]}...")
        return True

def test_azure_chat_connection():
    """Test Azure Chat OpenAI connection"""
    try:
        print("\n🔍 Testing Azure Chat OpenAI connection...")
        
        # Test with different API versions
        api_versions = [
            "2024-07-01-preview",
            "2024-06-01",
            "2024-05-01-preview",
            "2024-02-01"
        ]
        
        for api_version in api_versions:
            try:
                print(f"  Testing API version: {api_version}")
                llm = AzureChatOpenAI(
                    azure_endpoint=ENDPOINT,
                    api_key=os.getenv("GITHUB_TOKEN"),
                    api_version=api_version,
                    deployment_name="gpt-4o",
                    temperature=0.7,
                    max_tokens=100,
                    timeout=30,
                    max_retries=1
                )
                
                # Try a simple invoke call
                response = llm.invoke("Hello, this is a test message.")
                print(f"  ✅ API version {api_version} works!")
                print(f"  Response: {response.content[:100]}...")
                return True
                
            except Exception as e:
                print(f"  ❌ API version {api_version} failed: {str(e)[:100]}...")
                continue
        
        print("❌ All API versions failed")
        return False
        
    except Exception as e:
        print(f"❌ Azure Chat OpenAI connection failed: {e}")
        return False

def test_azure_embeddings_connection():
    """Test Azure Embeddings connection"""
    try:
        print("\n🔍 Testing Azure Embeddings connection...")
        
        client = EmbeddingsClient(
            endpoint=ENDPOINT,
            credential=AzureKeyCredential(os.getenv("GITHUB_TOKEN"))
        )
        
        # Test with a simple embedding request
        response = client.embed(
            input=["This is a test message"], 
            model="Cohere-embed-v3-english"
        )
        
        print("✅ Azure Embeddings connection successful!")
        print(f"  Embedding dimension: {len(response.embeddings[0].embedding)}")
        return True
        
    except Exception as e:
        print(f"❌ Azure Embeddings connection failed: {e}")
        return False

def test_available_models():
    """Test what models are available"""
    try:
        print("\n🔍 Testing available models...")
        
        # Try to get model information
        from azure.ai.inference import ChatCompletionsClient
        
        client = ChatCompletionsClient(
            endpoint=ENDPOINT,
            credential=AzureKeyCredential(os.getenv("GITHUB_TOKEN"))
        )
        
        print("✅ Successfully created ChatCompletionsClient")
        return True
        
    except Exception as e:
        print(f"❌ Failed to create ChatCompletionsClient: {e}")
        return False

def main():
    print("🚀 Starting Azure AI Studio API diagnostics...\n")
    
    # Test 1: Check environment variables
    if not test_github_token():
        print("\n❌ GitHub token is missing. Please check your .env file.")
        return
    
    # Test 2: Test Azure Chat connection
    test_azure_chat_connection()
    
    # Test 3: Test Azure Embeddings connection
    test_azure_embeddings_connection()
    
    # Test 4: Test available models
    test_available_models()
    
    print("\n✅ Diagnostics completed!")

if __name__ == "__main__":
    main()
