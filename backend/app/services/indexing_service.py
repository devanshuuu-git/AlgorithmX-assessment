import os
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_qdrant import QdrantVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from app.config import settings

class IndexingService:
    """
    Service dedicated to indexing documents (mirrors index.py).
    
    This service handles:
    1. Loading PDF files using PyPDFLoader
    2. Splitting text into chunks using RecursiveCharacterTextSplitter
    3. Generating embeddings using Google Gemini
    4. Indexing vectors into Qdrant
    """
    
    def __init__(self):
        """Initialize embeddings, text splitter, and Qdrant settings."""
        # Initialize Embeddings
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model=settings.embedding_model,
            google_api_key=settings.gemini_api_key
        )
        
        # Text Splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=300
        )
        
        self.qdrant_url = settings.qdrant_url
        self.collection_name = "pdf_rag_collection"

    async def index_file(self, file_path: str) -> int:
        """
        Load PDF -> Split -> Index in Qdrant.
        
        Args:
            file_path: Absolute path to the PDF file.
            
        Returns:
            int: Number of chunks indexed.
        """
        print(f"Loading PDF: {file_path}")
        loader = PyPDFLoader(file_path)
        docs = loader.load()
        
        print(f"Splitting {len(docs)} pages...")
        chunks = self.text_splitter.split_documents(docs)
        
        # Add metadata
        filename = Path(file_path).name
        for chunk in chunks:
            chunk.metadata["source"] = filename
            
        print(f"Indexing {len(chunks)} chunks to Qdrant...")
        QdrantVectorStore.from_documents(
            documents=chunks,
            embedding=self.embeddings,
            url=self.qdrant_url,
            collection_name=self.collection_name
        )
        print("Indexing done!")
        return len(chunks)

# Singleton instance
indexing_service = IndexingService()
