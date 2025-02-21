## This files contains RAG - Retrieval augemented generation frontend functionalities
## it relies on langchain, FAISS and vector database, embedding models such as cohere embed, openai embeddings etc 
from typing import List
from langchain_azure_ai.chat_models import AzureAIChatCompletionsModel
import os 
from langchain_cohere import CohereEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
from langchain.embeddings.base import Embeddings
from azure.ai.inference import EmbeddingsClient
from azure.core.credentials import AzureKeyCredential
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_openai import OpenAIEmbeddings
from sentence_transformers import SentenceTransformer
import CHAT_MODELS
import EMBEDDING_MODELS
from utils import  json_to_flattened_text, json_to_flattened_text_azure_ai, json_to_flattened_text_openai
from IPython.display import display, Markdown

from tqdm import tqdm  # for progress tracking
from langchain.schema import Document


ENDPOINT = "https://models.inference.ai.azure.com"
API_VERSION = "2024-12-12-preview"

class AzureAIChat:
    def __init__(self, chat_model: str):
        load_dotenv()
        self.CHAT_MODELS = CHAT_MODELS.ChatModel.get_all_models()
        if self.__validate_chat_model__(chat_model):
            self.llm = AzureAIChatCompletionsModel(
                endpoint=ENDPOINT,
                credential=os.getenv("GITHUB_TOKEN"),
                model_name=chat_model
            )
        else:
            raise ValueError(f"Chat model {chat_model} is not supported")
    
    def __validate_chat_model__(self, chat_model: str):
        if chat_model in self.CHAT_MODELS:
            return True
        else:
            return False

    def __call__(self):
        return self.llm
    
class CustomAzureEmbeddings(Embeddings):
    def __init__(self, model_name):
        load_dotenv()
        if not self.__validate_model__(model_name):
            raise ValueError(f"Model {model_name} is not supported")
        else:
            self.client = EmbeddingsClient(
                endpoint=ENDPOINT, 
                credential=AzureKeyCredential(os.getenv("GITHUB_TOKEN"))
            )
            self.model_name = model_name

    def __validate_model__(self, model_name):
        if model_name in EMBEDDING_MODELS.EmbeddingModel.get_all_models():
            return True
        else:
            return False
        
    def embed_documents(self, texts):
        # Handle batch size limit of 96
        chunk_size = 96
        all_embeddings = []
        
        for i in range(0, len(texts), chunk_size):
            chunk = texts[i:i + chunk_size]
            response = self.client.embed(input=chunk, model=self.model_name)
            embeddings = [item.embedding for item in response.data]
            all_embeddings.extend(embeddings)
        
        return all_embeddings
    
    def embed_query(self, text):
        response = self.client.embed(input=[text], model=self.model_name)
        return response.data[0].embedding

class SentenceTransformerWrapper(Embeddings):
    def __init__(self, model):
        self.model = SentenceTransformer(model)
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return self.model.encode(texts).tolist()
    
    def embed_query(self, text):
        return self.model.encode([text])[0].tolist()

class RAGFrontend:
    def __init__(self,embedding_model:str,json_file_path:str):
        self.EMBEDDING_MODELS = EMBEDDING_MODELS.EmbeddingModel.get_all_models()
        self.embedding_model = embedding_model
        self.json_file_path = json_file_path

    def __OpenAIEmbed__(self,embedding_model):
        return OpenAIEmbeddings(model=embedding_model)
    
    def __AzureAIEmbed__(self,embedding_model):
        return CustomAzureEmbeddings(embedding_model)
    
    def __SentenceTransformerEmbed__(self,embedding_model):
        return SentenceTransformerWrapper(model=embedding_model)
    
    def __validate_embedding_model__(self,embedding_model:str):
        if embedding_model in self.EMBEDDING_MODELS:
            return True
        else:
            return False
    
    def __get_embeddings__(self,embedding_model:str):
        if embedding_model == "text-embedding-3-large" or embedding_model == "text-embedding-3-small":
            return self.__OpenAIEmbed__(embedding_model)
        # elif embedding_model == "Cohere-embed-v3-multilingual" or embedding_model == "Cohere-embed-v3-english":
        #     return self.__CohereEmbed__(embedding_model)
        elif embedding_model == "Cohere-embed-v3-multilingual" or embedding_model == "Cohere-embed-v3-english":
            return self.__AzureAIEmbed__(embedding_model)
        else:
            return self.__SentenceTransformerEmbed__(embedding_model)
            
    def __flattened_text_from_json__(self) -> str:

        flattened_text = json_to_flattened_text(self.json_file_path)

        return flattened_text
    

    def create_vector_store(self) -> FAISS:
        """
        Creates a FAISS vector store using either OpenAI or SentenceTransformer embeddings.
        Handles large datasets by processing in batches and includes error handling.
        
        Returns:
            FAISS: A FAISS vector store containing the embedded documents
        """
        if not self.__validate_embedding_model__(self.embedding_model):
            raise ValueError(f"Invalid embedding model: {self.embedding_model}")

        try:
            # Get embeddings model
            embeddings = self.__get_embeddings__(self.embedding_model)
            
            # Get formatted text chunks
            chunks = self.__flattened_text_from_json__()
            if not chunks:
                raise ValueError("No text chunks were generated from the JSON file")

            print(f"Processing {len(chunks)} author profiles...")
            
            # Initialize vectorstore as None
            vectorstore = None
            
            if isinstance(embeddings, (SentenceTransformerWrapper, SentenceTransformer)):  # Add SentenceTransformer to check
                batch_size = 100
            else:
                batch_size = 50

            
            # Use tqdm for progress tracking
            for i in tqdm(range(0, len(chunks), batch_size), desc="Creating vector store"):
                batch = chunks[i:i + batch_size]
                
                # Create metadata for the batch
                batch_metadata = [
                    {
                        "source": f"author_{i + idx}",
                        "chunk_number": i + idx,
                        "batch_number": i // batch_size,
                        "model_type": "sentence_transformer" if isinstance(embeddings, SentenceTransformerWrapper) else "openai"
                    } 
                    for idx in range(len(batch))
                ]
                
                try:
                    if vectorstore is None:
                        # Create initial vectorstore
                        vectorstore = FAISS.from_texts(
                            texts=batch,
                            embedding=embeddings,
                            metadatas=batch_metadata
                        )
                    else:
                        # Create temporary vectorstore for the batch
                        batch_vectorstore = FAISS.from_texts(
                            texts=batch,
                            embedding=embeddings,
                            metadatas=batch_metadata
                        )
                        # Merge into main vectorstore
                        vectorstore.merge_from(batch_vectorstore)
                    
                except Exception as e:
                    print(f"Error processing batch {i // batch_size}: {str(e)}")
                    print(f"Skipping problematic batch and continuing...")
                    continue
            
            if vectorstore is None:
                raise ValueError("Failed to create vector store - all batches failed")
                
            print("Vector store creation completed successfully!")
            return vectorstore
            
        except Exception as e:
            print(f"Error creating vector store: {str(e)}")
            raise