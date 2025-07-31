#!/usr/bin/env python3
"""
Script to create vectorstores for different embedding models
"""

import os
import sys
from pathlib import Path
from rag import RAGFrontend

def check_json_file():
    """Check which JSON file exists and return the path"""
    possible_files = [
        "authors_with_h_index_new_11.json",  # Prioritize this file first
        "authors_with_h_index.json",
        "authors_cleaned.json"
    ]
    
    for file_path in possible_files:
        if Path(file_path).exists():
            print(f"✅ Found JSON file: {file_path}")
            return file_path
    
    print("❌ No JSON data file found. Please check one of these files exists:")
    for file_path in possible_files:
        print(f"   - {file_path}")
    return None

def create_vectorstore(embedding_model, json_file_path, custom_save_path=None):
    """Create vectorstore for a specific embedding model"""
    print(f"\n=== Creating vectorstore for {embedding_model} ===")
    
    try:
        # Create RAG frontend
        rag = RAGFrontend(
            embedding_model=embedding_model,
            json_file_path=json_file_path
        )
        
        # Create vectorstore
        print("Creating vector store...")
        vectorstore = rag.create_vector_store()
        
        if vectorstore is None:
            print(f"❌ Failed to create vectorstore for {embedding_model}")
            return False
        
        # Determine save path
        if custom_save_path:
            save_path = custom_save_path
        else:
            # Generate save path based on model name
            if embedding_model.startswith("Cohere-embed-v3"):
                save_path = f"{embedding_model.replace('-', '_')}_faiss_index"
            elif embedding_model.startswith("text-embedding-3"):
                save_path = f"{embedding_model.replace('-', '_')}_faiss_index"
            elif "sentence-transformers" in embedding_model:
                model_name = embedding_model.split("/")[-1]
                save_path = f"{model_name.replace('-', '_')}_faiss_index"
            else:
                save_path = f"{embedding_model.replace('-', '_').replace('/', '_')}_faiss_index"
        
        # Save the vectorstore
        print(f"Saving to: {save_path}")
        vectorstore.save_local(save_path)
        
        # Verify the save
        if Path(save_path).exists():
            print(f"✅ FAISS index saved successfully to {save_path}")
            return True
        else:
            print(f"❌ Failed to save FAISS index to {save_path}")
            return False
            
    except Exception as e:
        print(f"❌ Error creating vectorstore for {embedding_model}: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main function to create vectorstores"""
    print("TuniSci Vectorstore Creation Script")
    print("=" * 40)
    
    # Check for JSON file
    json_file_path = check_json_file()
    if not json_file_path:
        print("❌ Cannot proceed without JSON data file")
        sys.exit(1)
    
    # Available embedding models
    available_models = {
        "1": "Cohere-embed-v3-multilingual",
        "2": "Cohere-embed-v3-english", 
        "3": "text-embedding-3-large",
        "4": "text-embedding-3-small",
        "5": "sentence-transformers/paraphrase-MiniLM-L6-v2",
        "6": "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
        "7": "sentence-transformers/all-MiniLM-L6-v2"
    }
    
    print("\nAvailable embedding models:")
    for key, model in available_models.items():
        print(f"  {key}. {model}")
    print("  0. Create all models")
    
    # Get user choice
    choice = input("\nSelect embedding model (number): ").strip()
    
    if choice == "0":
        # Create all models
        print("\n🚀 Creating vectorstores for all models...")
        success_count = 0
        
        for model in available_models.values():
            if create_vectorstore(model, json_file_path):
                success_count += 1
        
        print(f"\n✅ Successfully created {success_count}/{len(available_models)} vectorstores")
        
    elif choice in available_models:
        # Create single model
        selected_model = available_models[choice]
        print(f"\n🚀 Creating vectorstore for {selected_model}...")
        
        if create_vectorstore(selected_model, json_file_path):
            print("\n✅ Vectorstore creation completed successfully!")
        else:
            print("\n❌ Vectorstore creation failed!")
            sys.exit(1)
    
    else:
        print("❌ Invalid choice")
        sys.exit(1)

if __name__ == "__main__":
    main()

