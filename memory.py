import os
import faiss
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

# I've switched to HuggingFace local embeddings (all-MiniLM-L6-v2).
# This is great because:
# 1. It's free and runs on your CPU.
# 2. It doesn't need an API key for every vector search.
# 3. It makes the research agent truly autonomous and local-friendly.
class ResearchMemory:
    def __init__(self, index_path="research_outputs/faiss_index"):
        self.index_path = index_path
        # Using a small, efficient model that handles research text well.
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.vector_db = None
        
        if os.path.exists(index_path):
            try:
                self.vector_db = FAISS.load_local(
                    index_path, 
                    self.embeddings, 
                    allow_dangerous_deserialization=True
                )
            except Exception as e:
                print(f"Note: Could not load existing memory ({e}). Starting fresh.")

    def add_fact(self, fact: str, source: str = "research"):
        """Stores a new research finding in the local brain."""
        doc = Document(page_content=fact, metadata={"source": source})
        if self.vector_db is None:
            self.vector_db = FAISS.from_documents([doc], self.embeddings)
        else:
            self.vector_db.add_documents([doc])
        
        # Ensure the knowledge persists between agent loops.
        self.vector_db.save_local(self.index_path)

    def query(self, query: str, k: int = 5):
        """Finds previously discovered facts related to a new question."""
        if self.vector_db is None:
            return []
        docs = self.vector_db.similarity_search(query, k=k)
        return [doc.page_content for doc in docs]

    def clear(self):
        """Clears all stored knowledge for a new project."""
        if os.path.exists(self.index_path):
            import shutil
            shutil.rmtree(self.index_path)
            self.vector_db = None
