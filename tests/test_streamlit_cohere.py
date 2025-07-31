#!/usr/bin/env python3
"""
Test streamlit app with Cohere embedding
"""

import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from dotenv import load_dotenv

# Load environment
load_dotenv()

def test_streamlit_cohere_loading():
    """Test if streamlit can load Cohere embedding correctly"""
    print("=== Testing Streamlit Cohere Integration ===")
    
    try:
        # Import streamlit app functions
        from streamlit_app import load_rag_components
        
        # Mock streamlit functions
        class MockStreamlit:
            @staticmethod
            def error(msg):
                print(f"ST ERROR: {msg}")
            
            @staticmethod
            def success(msg):
                print(f"ST SUCCESS: {msg}")
            
            @staticmethod
            def spinner(msg):
                return MockContext()
            
            @staticmethod
            def expander(title):
                return MockContext()
            
            @staticmethod
            def code(text):
                print(f"ST CODE: {text}")
        
        class MockContext:
            def __enter__(self):
                return self
            def __exit__(self, *args):
                pass
        
        # Replace streamlit with mock
        import streamlit_app
        original_st = streamlit_app.st
        streamlit_app.st = MockStreamlit()
        
        try:
            # Test loading Cohere embedding
            print("Testing Cohere embedding loading...")
            retriever = load_rag_components("Cohere-embed-v3-multilingual")
            
            if retriever:
                print("✅ Cohere embedding loaded successfully in streamlit context")
                
                # Test a simple retrieval
                test_query = "computer science professor"
                results = retriever.invoke(test_query)
                print(f"✅ Retrieved {len(results)} documents")
                print(f"Sample result: {results[0].page_content[:100]}...")
                
                return True
            else:
                print("❌ Cohere embedding loading failed")
                return False
                
        finally:
            # Restore original streamlit
            streamlit_app.st = original_st
            
    except Exception as e:
        print(f"❌ Streamlit Cohere test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_chat_with_cohere():
    """Test the complete chat functionality with Cohere"""
    print("\n=== Testing Chat with Cohere Embedding ===")
    
    try:
        from streamlit_app import load_rag_components, query_chat_model
        from rag import AzureAIChat
        
        # Mock streamlit
        class MockStreamlit:
            @staticmethod
            def error(msg):
                print(f"ST ERROR: {msg}")
            @staticmethod
            def success(msg):
                print(f"ST SUCCESS: {msg}")
            @staticmethod
            def warning(msg):
                print(f"ST WARNING: {msg}")
            @staticmethod
            def spinner(msg):
                return MockContext()
            @staticmethod
            def expander(title):
                return MockContext()
            @staticmethod
            def code(text):
                print(f"ST CODE: {text}")
        
        class MockContext:
            def __enter__(self):
                return self
            def __exit__(self, *args):
                pass
        
        import streamlit_app
        original_st = streamlit_app.st
        streamlit_app.st = MockStreamlit()
        
        try:
            # Load Cohere retriever
            retriever = load_rag_components("Cohere-embed-v3-multilingual")
            if not retriever:
                print("❌ Could not load Cohere retriever")
                return False
            
            # Test chat with Cohere retriever
            test_query = "Who are some professors in computer science?"
            selected_model = "gpt-4o-mini"
            
            print(f"Testing chat with query: '{test_query}'")
            print(f"Using model: {selected_model}")
            
            # This would normally show spinners in streamlit
            response, model_used = query_chat_model(test_query, retriever, selected_model)
            
            if response:
                print("✅ Chat with Cohere embedding successful!")
                print(f"Model used: {model_used}")
                print(f"Response preview: {response[:150]}...")
                return True
            else:
                print("❌ Chat response was None")
                return False
                
        finally:
            streamlit_app.st = original_st
            
    except Exception as e:
        print(f"❌ Chat test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Testing Streamlit Cohere Integration")
    print("=" * 40)
    
    # Test 1: Basic loading
    if not test_streamlit_cohere_loading():
        print("❌ Basic loading test failed")
        exit(1)
    
    # Test 2: Complete chat functionality
    test_chat_with_cohere()
    
    print("\n" + "=" * 40)
    print("Integration test complete!")
