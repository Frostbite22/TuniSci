
import enum

class EmbeddingModel(enum.Enum):
    TEXT_EMBEDDING_3_LARGE = "text-embedding-3-large"
    TEXT_EMBEDDING_3_SMALL = "text-embedding-3-small"
    COHERE_EMBED_V3_MULTILINGUAL = "Cohere-embed-v3-multilingual"
    COHERE_EMBED_V3_ENGLISH = "Cohere-embed-v3-english"
    PARAPHRASE_MULTILINGUAL_MINILM_L12_V2 = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    PARAPHRASE_MULTILINGUAL_MINILM_L6_V2 = "sentence-transformers/paraphrase-multilingual-MiniLM-L6-v2"

    def __str__(self):
        return self.value
    
    def __repr__(self):
        return self.value
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)
    
    @classmethod
    def get_all_models(cls):
        return [item.value for item in cls]
    
    @classmethod
    def get_model(cls, model_name):
        for item in cls:
            if model_name == item.value:
                return item
        return None
    
## how to call this class
# print(EmbeddingModel.TEXT_EMBEDDING_3_LARGE)
# print(EmbeddingModel.TEXT_EMBEDDING_3_LARGE.value)
# print(EmbeddingModel.has_value("text-embedding-3-large"))
# print(EmbeddingModel.get_all_models())
# print(EmbeddingModel.get_model("text-embedding-3-large"))
