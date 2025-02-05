## This files contains RAG - Retrieval augemented generation frontend functionalities
## it relies on langchain, FAISS and vector database, embedding models such as cohere embed, openai embeddings etc 
from langchain_azure_ai.chat_models import AzureAIChatCompletionsModel
import os 
from langchain_text_splitters import RecursiveCharacterTextSplitter
import load_dotenv
from langchain.embeddings.base import Embeddings
from azure.ai.inference import EmbeddingsClient
from azure.core.credentials import AzureKeyCredential
from langchain.vectorstores import FAISS

from langchain_openai import OpenAIEmbeddings

import CHAT_MODELS
import EMBEDDING_MODELS
from utils import json_to_flattened_text



ENDPOINT = "https://models.inference.ai.azure.com"
API_VERSION = "2024-05-01-preview"

class AzureAIChat:
    def __init__(self,model_name:str):
        self.llm = AzureAIChatCompletionsModel(
            endpoint=ENDPOINT,
            token = load_dotenv("GITHUB_TOKEN"),
            model_name=model_name,
            api_version=API_VERSION
        )

class CustomAzureEmbeddings(Embeddings):
    def __init__(self, model_name):
        self.client = EmbeddingsClient(endpoint=ENDPOINT, credential=AzureKeyCredential(load_dotenv("GITHUB_TOKEN")))
        self.model_name = model_name
        
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
    

class RAGFrontend:
    def __init__(self,embedding_model:str,chat_model:str,json_file_path:str,query:str):
        self.CHAT_MODELS = CHAT_MODELS.get_all_models()
        self.EMBEDDING_MODELS = EMBEDDING_MODELS.get_all_models()
        self.embedding_model = embedding_model
        self.chat_model = chat_model
        self.json_file_path = json_file_path
        self.query = query

    def __OpenAIEmbed__(self,model_name):
        return OpenAIEmbeddings(model=model_name)
    
    def __AzureAIEmbed__(self,model_name):
        return CustomAzureEmbeddings(model_name)
    
    def __AzureAIChat__(self,model_name):
        return AzureAIChat(model_name)
    
    def __validate_chat_model__(self,chat_model:str):
        if chat_model in self.CHAT_MODELS:
            return True
        else:
            return False
    
    def __validate_embedding_model__(self,embedding_model:str):
        if embedding_model in self.EMBEDDING_MODELS:
            return True
        else:
            return False
    
    def __get_embeddings__(self,embedding_model:str):
        if embedding_model == "text-embedding-3-large" or embedding_model == "text-embedding-3-small":
            return self.__OpenAIEmbed__(embedding_model)
        else:
            return self.__AzureAIEmbed__(embedding_model)
        
    def __get_chat_model__(self,chat_model:str):
        return self.__AzureAIChat__(chat_model)
    
    def __flattened_text_from_json__(self) -> str:
        flattened_text = json_to_flattened_text(self.json_file_path)
        return flattened_text
    
    def create_vector_store(self):
        """
        Creates a FAISS vector store from text documents using specified embedding model.

        This function processes text documents and creates a searchable vector store using FAISS.
        It handles different embedding models and applies appropriate text splitting strategies
        based on the model type.

        Parameters:
            texts (list): List of text documents to be embedded.

        Returns:
            FAISS: A FAISS vector store containing the embedded documents.

        Raises:
            ValueError: If the embedding model is not valid or not supported.

        Notes:
            - For 'text-embedding-3-large' and 'text-embedding-3-small' models:
                * Uses chunk size of 190 with 10 token overlap
                * Applies recursive character text splitting
            - For other embedding models:
                * CustomAzrueEmbeddings handles the chunking and embedding
                * Includes source metadata for each document
        """
        if self.__validate_embedding_model__(self.embedding_model):
            embeddings = self.__get_embeddings__(self.embedding_model)
            flattened_text = self.__flattened_text_from_json__()
            if self.embedding_model == "text-embedding-3-large" or self.embedding_model == "text-embedding-3-small":
                text_splitter = RecursiveCharacterTextSplitter(chunk_size=190, chunk_overlap=10)
                chunks = text_splitter.split_text(flattened_text)
                vectorstore = FAISS.from_texts(chunks, embeddings)
                return vectorstore
            else :
                # Create FAISS index with the custom embedding function
                vectorstore = FAISS.from_texts(
                    texts=flattened_text,
                    embedding=embeddings,
                    metadatas=[{"source": str(i)} for i in range(len(flattened_text))]
                )
                return vectorstore
    
    
