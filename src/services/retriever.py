"""
Vector Database Service using FAISS for RAG
"""
import faiss
import numpy as np
import pickle
import os
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any
from src.config import settings
import logging

logger = logging.getLogger(__name__)

class VectorDB:
    def __init__(self):
        """Initialize FAISS index and embedding model"""
        self._encoder = None
        self.index = None
        self.documents = []  # Stores metadata corresponding to vectors
        
        # Load existing index if available
        self._load_index()

    @property
    def encoder(self):
        """Lazy load encoder"""
        if self._encoder is None:
            logger.info("Loading embedding model...")
            self._encoder = SentenceTransformer(settings.embedding_model)
        return self._encoder

    def _load_index(self):
        """Load FAISS index from disk"""
        index_file = os.path.join(settings.faiss_index_path, "index.faiss")
        docs_file = os.path.join(settings.faiss_index_path, "documents.pkl")
        
        if os.path.exists(index_file) and os.path.exists(docs_file):
            logger.info("Loading existing FAISS index...")
            self.index = faiss.read_index(index_file)
            with open(docs_file, "rb") as f:
                self.documents = pickle.load(f)
        else:
            logger.info("Initializing new FAISS index...")
            # Valid dimension for all-MiniLM-L6-v2 is 384
            self.index = faiss.IndexFlatL2(384) 
            self.documents = []

    def save_index(self):
        """Save FAISS index and documents to disk"""
        os.makedirs(settings.faiss_index_path, exist_ok=True)
        
        index_file = os.path.join(settings.faiss_index_path, "index.faiss")
        docs_file = os.path.join(settings.faiss_index_path, "documents.pkl")
        
        faiss.write_index(self.index, index_file)
        with open(docs_file, "wb") as f:
            pickle.dump(self.documents, f)
            
    def add_documents(self, docs: List[Dict[str, Any]]):
        """
        Add documents to vector DB
        
        Args:
            docs: List of dicts with 'text' and 'id' keys
        """
        texts = [doc['text'] for doc in docs]
        if not texts:
            return
            
        embeddings = self.encoder.encode(texts)
        self.index.add(np.array(embeddings).astype('float32'))
        self.documents.extend(docs)
        self.save_index()
        logger.info(f"Added {len(docs)} documents to vector DB")

    def search(self, query: str, k: int = 3) -> List[Dict[str, Any]]:
        """
        Search for relevant documents
        
        Args:
            query: User query string
            k: Number of results to return
            
        Returns:
            List of relevant documents with scores
        """
        if self.index.ntotal == 0:
            return []
            
        query_vector = self.encoder.encode([query])
        distances, indices = self.index.search(np.array(query_vector).astype('float32'), k)
        
        results = []
        for i, idx in enumerate(indices[0]):
            if idx != -1 and idx < len(self.documents):
                doc = self.documents[idx].copy()
                doc['score'] = float(distances[0][i])
                results.append(doc)
                
        return results

# Global VectorDB instance
vector_db = VectorDB()
