from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer
import warnings
import sys

# Suppress HuggingFace/PyTorch spam on startup
warnings.filterwarnings("ignore")

class SemanticEmbedder:
    _instance = None
    
    def __new__(cls):
        """Singleton pattern so the 80MB model is only loaded into RAM once."""
        if cls._instance is None:
            cls._instance = super(SemanticEmbedder, cls).__new__(cls)
            try:
                # Load the specified model in CPU mode
                print("Loading Sentence-BERT model (all-MiniLM-L6-v2)...", file=sys.stderr)
                cls._instance.model = SentenceTransformer('all-MiniLM-L6-v2')
            except Exception as e:
                print(f"Error loading SBERT: {e}", file=sys.stderr)
                cls._instance.model = None
        return cls._instance
        
    def embed_text(self, text: str) -> List[float]:
        """Runs the text through SBERT with mean-pooling for long texts (>250 tokens)."""
        if not self.model or not text.strip():
            return [0.0] * 384
            
        # Fix #1: Handle Token Limits via Chunking & Mean Pooling
        # Split text into chunks of approx ~200 words to stay well within 256 tokens
        words = text.split()
        chunk_size = 200
        chunks = [" ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]
        
        if not chunks:
             return [0.0] * 384
             
        # Encode all chunks. Sentences-transformers handles batch encoding natively.
        vectors = self.model.encode(chunks)
        
        # If there's only one chunk, avoid the math overhead
        if len(vectors) == 1:
            return vectors[0].tolist()
            
        # Mean pooling: Average the embeddings across the axis 0
        pooled_vector = np.mean(vectors, axis=0)
        return pooled_vector.tolist()

# Pre-initialize on module load in the worker process
embedder = SemanticEmbedder()
