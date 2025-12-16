from langchain_qdrant import QdrantVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from qdrant_client import QdrantClient, models
from typing import List, Optional, Dict, Any

from app.config import settings

class RetrievalService:
    """
    Service dedicated to retrieving relevant documents from Qdrant.
    Handles vector search, filtering, and top_k configuration.
    """
    
    def __init__(self):
        # Initialize Embeddings
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model=settings.embedding_model,
            google_api_key=settings.gemini_api_key
        )
        
        self.qdrant_url = settings.qdrant_url
        self.collection_name = "pdf_rag_collection"
        self.client = QdrantClient(url=self.qdrant_url)

    async def search(
        self, 
        query: str, 
        top_k: int = 4, 
        doc_filename: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Perform similarity search with optional filtering.
        
        Args:
            query: The user's search query.
            top_k: Number of chunks to retrieve.
            doc_filename: Optional filename to filter by.
            
        Returns:
            List of dictionaries containing page_content and metadata.
        """
        print(f"🔍 Searching for: '{query}' (top_k={top_k}, filter={doc_filename})")
        
        # Construct Qdrant Filter if doc_filename is provided
        qdrant_filter = None
        if doc_filename and doc_filename != "All Documents":
            qdrant_filter = models.Filter(
                must=[
                    models.FieldCondition(
                        key="metadata.source",
                        match=models.MatchValue(value=doc_filename)
                    )
                ]
            )

        # Use LangChain's Qdrant wrapper for convenience, but we could use client directly too
        vector_store = QdrantVectorStore.from_existing_collection(
            embedding=self.embeddings,
            collection_name=self.collection_name,
            url=self.qdrant_url
        )
        
        # Perform search
        # Note: LangChain's similarity_search accepts a filter argument for Qdrant
        results = vector_store.similarity_search(
            query, 
            k=top_k,
            filter=qdrant_filter
        )
        
        # Format results
        formatted_results = []
        for doc in results:
            formatted_results.append({
                "page_content": doc.page_content,
                "metadata": doc.metadata
            })
            
        return formatted_results

# Singleton instance
retrieval_service = RetrievalService()
