## We are trying open embedding models from huggingface and sentence transformers 
from sentence_transformers import SentenceTransformer

sentences = ['This framework generates embeddings for each input sentence',
             'Sentences are passed as a list of string.',
             'The quick brown fox jumps over the lazy dog.']

model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
embeddings = model.encode(sentences)
print(len(embeddings[0]))
