import os
from typing import List, Dict
import logging

# Optional imports for RAG
try:
    import chromadb
    from chromadb.config import Settings
    from sentence_transformers import SentenceTransformer
except ImportError:
    chromadb = None
    SentenceTransformer = None

class RAGManager:
    def __init__(self, persist_dir: str = None):
        self.enabled = chromadb is not None and SentenceTransformer is not None
        if not self.enabled:
            return

        if persist_dir is None:
            persist_dir = os.path.join(os.path.expanduser("~"), ".nexus", "rag_db")
        
        self.persist_dir = persist_dir
        os.makedirs(self.persist_dir, exist_ok=True)
        
        try:
            self.client = chromadb.PersistentClient(path=self.persist_dir)
            self.collection = self.client.get_or_create_collection(name="nexus_knowledge")
            # Use a small, fast model
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
        except Exception as e:
            logging.error(f"RAG Init Error: {e}")
            self.enabled = False

    def add_document(self, doc_id: str, text: str, metadata: Dict = None):
        if not self.enabled:
            return False
        
        try:
            embedding = self.model.encode(text).tolist()
            self.collection.add(
                ids=[doc_id],
                embeddings=[embedding],
                documents=[text],
                metadatas=[metadata or {}]
            )
            return True
        except Exception as e:
            logging.error(f"RAG Add Error: {e}")
            return False

    def query(self, query_text: str, n_results: int = 3) -> List[str]:
        if not self.enabled:
            return []
            
        try:
            embedding = self.model.encode(query_text).tolist()
            results = self.collection.query(
                query_embeddings=[embedding],
                n_results=n_results
            )
            return results['documents'][0] if results['documents'] else []
        except Exception as e:
            logging.error(f"RAG Query Error: {e}")
            return []
