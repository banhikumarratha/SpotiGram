from sentence_transformers import SentenceTransformer
from typing import List

class EmbeddingLogic:
    def __init__(self):
        # Local, lightweight model
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def generate_embedding(self, text: str) -> List[float]:
        embedding = self.model.encode(text)
        return embedding.tolist()
