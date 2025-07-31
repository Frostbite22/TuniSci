#!/usr/bin/env python3
"""
Summary of available vectorstores and models
"""

import os
from pathlib import Path

def check_vectorstores():
    """Check what vectorstores are available"""
    print("=== Available Vectorstores ===")
    
    vectorstore_folders = [f for f in os.listdir('.') if f.endswith('_faiss_index')]
    
    if not vectorstore_folders:
        print("❌ No vectorstore folders found")
        return []
    
    for folder in vectorstore_folders:
        print(f"✅ {folder}")
        
        # Check folder contents
        files = os.listdir(folder)
        print(f"   Files: {', '.join(files)}")
        
        # Check size
        total_size = sum(os.path.getsize(os.path.join(folder, f)) for f in files)
        print(f"   Size: {total_size / (1024*1024):.1f} MB")
        print()
    
    return vectorstore_folders

def check_streamlit_config():
    """Check streamlit app configuration"""
    print("=== Streamlit App Configuration ===")
    
    try:
        import streamlit_app
        
        print("Embedding Models:")
        for model, folder in streamlit_app.EMBEDDING_MODELS.items():
            exists = "✅" if os.path.exists(folder) else "❌"
            print(f"  {exists} {model} → {folder}")
        
        print("\nChat Models:")
        for model in streamlit_app.CHAT_MODELS:
            print(f"  📝 {model}")
            
    except Exception as e:
        print(f"❌ Could not load streamlit config: {e}")

def check_environment():
    """Check environment setup"""
    print("=== Environment Setup ===")
    
    # Check .env file
    if Path(".env").exists():
        print("✅ .env file found")
    else:
        print("❌ .env file not found")
    
    # Check GitHub token
    github_token = os.getenv("GITHUB_TOKEN")
    if github_token:
        print(f"✅ GITHUB_TOKEN found (length: {len(github_token)})")
    else:
        print("❌ GITHUB_TOKEN not found")
    
    # Check JSON data file
    if Path("authors_with_h_index.json").exists():
        print("✅ authors_with_h_index.json found")
    else:
        print("❌ authors_with_h_index.json not found")

if __name__ == "__main__":
    print("TuniSci Project Status")
    print("=" * 40)
    
    check_environment()
    print()
    check_vectorstores()
    print()
    check_streamlit_config()
    
    print("=" * 40)
    print("✅ Project setup complete!")
    print("\nTo run the app:")
    print("poetry run streamlit run streamlit_app.py")
