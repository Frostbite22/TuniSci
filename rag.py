## This files contains RAG - Retrieval augemented generation frontend functionalities
## it relies on langchain, FAISS and vector database, embedding models such as cohere embed, openai embeddings etc 
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
import CHAT_MODELS
import EMBEDDING_MODELS
from utils import  json_to_flattened_text_azure_ai, json_to_flattened_text_openai
from IPython.display import display, Markdown


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
    

class RAGFrontend:
    def __init__(self,embedding_model:str,json_file_path:str):
        self.EMBEDDING_MODELS = EMBEDDING_MODELS.EmbeddingModel.get_all_models()
        self.embedding_model = embedding_model
        self.json_file_path = json_file_path

    def __OpenAIEmbed__(self,embedding_model):
        return OpenAIEmbeddings(model=embedding_model)
    
    def __AzureAIEmbed__(self,embedding_model):
        return CustomAzureEmbeddings(embedding_model)
    

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
        else:
            return self.__AzureAIEmbed__(embedding_model)
            
    def __flattened_text_from_json__(self) -> str:
        if self.embedding_model == "text-embedding-3-large" or self.embedding_model == "text-embedding-3-small" :
            flattened_text = json_to_flattened_text_openai(self.json_file_path)
        else : 
            flattened_text = json_to_flattened_text_azure_ai(self.json_file_path)

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
            if self.embedding_model == "text-embedding-3-large" or self.embedding_model == "text-embedding-3-small" :
                text_splitter = RecursiveCharacterTextSplitter(chunk_size=190, chunk_overlap=20)
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


