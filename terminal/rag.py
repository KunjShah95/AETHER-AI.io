import os
from typing import List, Dict, Optional
import logging
import requests
import hashlib
from datetime import datetime

# Optional imports for RAG and processing
try:
    import chromadb
    from chromadb.config import Settings
    from sentence_transformers import SentenceTransformer
    from bs4 import BeautifulSoup
    import PyPDF2
except ImportError:
    chromadb = None
    SentenceTransformer = None
    BeautifulSoup = None
    PyPDF2 = None

class RAGManager:
    def __init__(self, persist_dir: str = None):
        self.enabled = chromadb is not None and SentenceTransformer is not None
        if not self.enabled:
            logging.warning("RAG dependencies missing. RAG features disabled.")
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

    def ingest_file(self, file_path: str) -> str:
        """Ingest a local file (txt, md, pdf) into the knowledge base."""
        if not self.enabled:
            return "❌ RAG is not enabled."
        
        if not os.path.exists(file_path):
            return f"❌ File not found: {file_path}"

        try:
            text = ""
            ext = os.path.splitext(file_path)[1].lower()
            
            if ext == '.pdf':
                if PyPDF2 is None:
                    return "❌ PyPDF2 not installed."
                with open(file_path, 'rb') as f:
                    reader = PyPDF2.PdfReader(f)
                    for page in reader.pages:
                        text += page.extract_text() + "\n"
            else:
                # Assume text-based
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    text = f.read()

            if not text.strip():
                return "⚠️ File is empty or could not be read."

            # Chunking (simple)
            chunk_size = 1000
            chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
            
            count = 0
            for i, chunk in enumerate(chunks):
                doc_id = f"file_{hashlib.md5(file_path.encode()).hexdigest()}_{i}"
                meta = {
                    "source": file_path,
                    "type": "file",
                    "timestamp": datetime.now().isoformat()
                }
                if self.add_document(doc_id, chunk, meta):
                    count += 1
            
            return f"✅ Ingested {count} chunks from {os.path.basename(file_path)}"

        except Exception as e:
            return f"❌ Error ingesting file: {str(e)}"

    def ingest_url(self, url: str) -> str:
        """Scrape and ingest a URL."""
        if not self.enabled:
            return "❌ RAG is not enabled."
        
        if BeautifulSoup is None:
            return "❌ BeautifulSoup not installed."

        try:
            response = requests.get(url, timeout=10)
            if response.status_code != 200:
                return f"❌ Failed to fetch URL: {response.status_code}"

            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()

            text = soup.get_text()
            # Break into lines and remove leading/trailing space on each
            lines = (line.strip() for line in text.splitlines())
            # Break multi-headlines into a line each
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            # Drop blank lines
            text = '\n'.join(chunk for chunk in chunks if chunk)

            # Chunking
            chunk_size = 1000
            text_chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
            
            count = 0
            for i, chunk in enumerate(text_chunks):
                doc_id = f"url_{hashlib.md5(url.encode()).hexdigest()}_{i}"
                meta = {
                    "source": url,
                    "type": "web",
                    "title": soup.title.string if soup.title else url,
                    "timestamp": datetime.now().isoformat()
                }
                if self.add_document(doc_id, chunk, meta):
                    count += 1
            
            return f"✅ Ingested {count} chunks from {url}"

        except Exception as e:
            return f"❌ Error ingesting URL: {str(e)}"

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
