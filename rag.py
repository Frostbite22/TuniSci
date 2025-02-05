## This files contains RAG - Retrieval augemented generation frontend functionalities
## it relies on langchain, FAISS and vector database, embedding models such as cohere embed, openai embeddings etc 
from langchain_azure_ai.chat_models import AzureAIChatCompletionsModel
import os 
import load_dotenv
from langchain.embeddings.base import Embeddings
from azure.ai.inference import EmbeddingsClient
from azure.core.credentials import AzureKeyCredential
from langchain.vectorstores import FAISS

from langchain_openai import OpenAIEmbeddings

import CHAT_MODELS
import EMBEDDING_MODELS



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
    def __init__(self,embedding_model:str,chat_model:str):
        self.CHAT_MODELS = CHAT_MODELS.get_all_models()
        self.EMBEDDING_MODELS = EMBEDDING_MODELS.get_all_models()
        self.embedding_model = embedding_model
        self.chat_model = chat_model

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