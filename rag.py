from typing import List
from dotenv import load_dotenv
import os
from tqdm import tqdm

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.embeddings.base import Embeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_openai import OpenAIEmbeddings, AzureOpenAIEmbeddings, AzureChatOpenAI
from sentence_transformers import SentenceTransformer
from langchain.schema import Document
from langchain.llms.base import LLM
from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.schema import BaseMessage

from azure.ai.inference import EmbeddingsClient, ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential

import CHAT_MODELS
import EMBEDDING_MODELS
from utils import json_to_flattened_text
from IPython.display import display, Markdown

ENDPOINT = "https://models.inference.ai.azure.com"

class AzureAIStudioLLM(LLM):
    """Custom LangChain wrapper for Azure AI Studio models"""
    
    model_name: str = ""
    endpoint: str = ""
    api_key: str = ""
    client: object = None
    
    def __init__(self, model_name: str, endpoint: str, api_key: str, **kwargs):
        # Initialize the fields before calling super().__init__
        kwargs['model_name'] = model_name
        kwargs['endpoint'] = endpoint
        kwargs['api_key'] = api_key
        kwargs['client'] = None  # Will be set after super init
        super().__init__(**kwargs)
        
        # Create the client after initialization
        self.client = ChatCompletionsClient(
            endpoint=endpoint,
            credential=AzureKeyCredential(api_key)
        )
    
    @property
    def _llm_type(self) -> str:
        return "azure_ai_studio"
    
    def _call(
        self,
        prompt: str,
        stop: List[str] = None,
        run_manager: CallbackManagerForLLMRun = None,
        **kwargs
    ) -> str:
        try:
            messages = [{"role": "user", "content": prompt}]
            response = self.client.complete(
                messages=messages,
                model=self.model_name,
                max_tokens=kwargs.get("max_tokens", 1000),
                temperature=kwargs.get("temperature", 0.7)
            )
            return response.choices[0].message.content
        except Exception as e:
            raise ValueError(f"Error calling Azure AI Studio model {self.model_name}: {str(e)}")

class AzureAIChat:
    def __init__(self, chat_model: str):
        load_dotenv()
        self.CHAT_MODELS = CHAT_MODELS.ChatModel.get_all_models()
        if self.__validate_chat_model__(chat_model):
            # Use our custom Azure AI Studio LLM wrapper
            self.llm = AzureAIStudioLLM(
                model_name=chat_model,
                endpoint=ENDPOINT,
                api_key=os.getenv("GITHUB_TOKEN"),
                temperature=0.7,
                max_tokens=1000
            )
        else:
            raise ValueError(f"Chat model {chat_model} is not supported")

    def __validate_chat_model__(self, chat_model: str):
        return chat_model in self.CHAT_MODELS

    def __call__(self):
        return self.llm

class CustomAzureEmbeddings(Embeddings):
    def __init__(self, model_name):
        load_dotenv()
        if not self.__validate_model__(model_name):
            raise ValueError(f"Model {model_name} is not supported")
        self.client = EmbeddingsClient(
            endpoint=ENDPOINT,
            credential=AzureKeyCredential(os.getenv("GITHUB_TOKEN"))
        )
        self.model_name = model_name

    def __validate_model__(self, model_name):
        return model_name in EMBEDDING_MODELS.EmbeddingModel.get_all_models()

    def embed_documents(self, texts):
        chunk_size = 96
        all_embeddings = []
        for i in range(0, len(texts), chunk_size):
            chunk = texts[i:i + chunk_size]
            response = self.client.embed(input=chunk, model=self.model_name)
            # Fixed: Use 'data' instead of 'embeddings' for the new API response format
            embeddings = [item.embedding for item in response.data]
            all_embeddings.extend(embeddings)
        return all_embeddings

    def embed_query(self, text):
        response = self.client.embed(input=[text], model=self.model_name)
        # Fixed: Use 'data' instead of 'embeddings' for the new API response format
        return response.data[0].embedding

class SentenceTransformerWrapper(Embeddings):
    def __init__(self, model):
        self.model = SentenceTransformer(model)

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return self.model.encode(texts).tolist()

    def embed_query(self, text):
        return self.model.encode([text])[0].tolist()

class RAGFrontend:
    def __init__(self, embedding_model: str, json_file_path: str):
        self.EMBEDDING_MODELS = EMBEDDING_MODELS.EmbeddingModel.get_all_models()
        self.embedding_model = embedding_model
        self.json_file_path = json_file_path

    def __OpenAIEmbed__(self, embedding_model):
        return OpenAIEmbeddings(model=embedding_model)

    def __AzureAIEmbed__(self, embedding_model):
        return CustomAzureEmbeddings(embedding_model)

    def __SentenceTransformerEmbed__(self, embedding_model):
        return SentenceTransformerWrapper(model=embedding_model)

    def __validate_embedding_model__(self, embedding_model: str):
        return embedding_model in self.EMBEDDING_MODELS

    def __get_embeddings__(self, embedding_model: str):
        if embedding_model.startswith("text-embedding-3"):
            return self.__OpenAIEmbed__(embedding_model)
        elif embedding_model.startswith("Cohere-embed-v3"):
            return self.__AzureAIEmbed__(embedding_model)
        else:
            return self.__SentenceTransformerEmbed__(embedding_model)

    def __flattened_text_from_json__(self) -> str:
        return json_to_flattened_text(self.json_file_path)

    def create_vector_store(self) -> FAISS:
        if not self.__validate_embedding_model__(self.embedding_model):
            raise ValueError(f"Invalid embedding model: {self.embedding_model}")

        try:
            embeddings = self.__get_embeddings__(self.embedding_model)
            chunks = self.__flattened_text_from_json__()
            if not chunks:
                raise ValueError("No text chunks were generated from the JSON file")

            print(f"Processing {len(chunks)} author profiles...")

            vectorstore = None
            batch_size = 100 if isinstance(embeddings, SentenceTransformerWrapper) else 50

            for i in tqdm(range(0, len(chunks), batch_size), desc="Creating vector store"):
                batch = chunks[i:i + batch_size]
                batch_metadata = [
                    {
                        "source": f"author_{i + idx}",
                        "chunk_number": i + idx,
                        "batch_number": i // batch_size,
                        "model_type": "sentence_transformer" if isinstance(embeddings, SentenceTransformerWrapper) else "openai"
                    } for idx in range(len(batch))
                ]

                try:
                    batch_vectorstore = FAISS.from_texts(
                        texts=batch,
                        embedding=embeddings,
                        metadatas=batch_metadata
                    )
                    if vectorstore is None:
                        vectorstore = batch_vectorstore
                    else:
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
