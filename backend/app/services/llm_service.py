from langchain_google_genai import ChatGoogleGenerativeAI
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Any, Optional
import time

from app.config import settings
from app.services.retrieval_service import retrieval_service
from app.models.models import Metric

class LLMService:
    """
    Service dedicated to generating answers using the LLM.
    Orchestrates Retrieval -> Generation -> Metrics Logging.
    """
    
    def __init__(self):
        self.default_model = settings.gemini_model
        self.api_key = settings.gemini_api_key

    async def generate_response(
        self, 
        query: str, 
        session_id: int,
        db: AsyncSession,
        model_name: str = "gemini-1.5-flash",
        top_k: int = 4,
        doc_filter: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate RAG response.
        
        Args:
            query: User question
            session_id: Current session ID (for metrics)
            db: Database session (for metrics)
            model_name: LLM model to use
            top_k: Number of chunks to retrieve
            doc_filter: Filename to filter by
            
        Returns:
            Dict with 'response' and 'context' (list of chunks)
        """
        start_time = time.time()
        
        # 1. Retrieve Context
        context_chunks = await retrieval_service.search(
            query=query,
            top_k=top_k,
            doc_filename=doc_filter
        )
        
        # 2. Check if context found (if strict mode enabled - logic can be added here)
        if not context_chunks:
            # We could implement "only answer if sources found" logic here
            pass

        # 3. Construct Prompt
        context_str = "\n\n".join([
            f"Source: {chunk['metadata'].get('source', 'Unknown')} (Page {chunk['metadata'].get('page', 'N/A')})\n"
            f"Content: {chunk['page_content']}"
            for chunk in context_chunks
        ])
        
        system_prompt = f"""
        You are a helpful AI Assistant. Answer the user's question based ONLY on the following context.
        If the answer is not in the context, say "I cannot answer this based on the provided documents."
        
        Include citations to the source file and page number in your answer (e.g., [Source: file.pdf, Page 2]).
        
        Context:
        {context_str}
        """
        
        # 4. Call LLM
        # Initialize LLM dynamically based on selected model
        llm = ChatGoogleGenerativeAI(
            model=model_name,
            google_api_key=self.api_key,
            temperature=0.3
        )
        
        messages = [
            ("system", system_prompt),
            ("user", query)
        ]
        
        response = await llm.ainvoke(messages)
        answer = response.content
        
        # 5. Log Metrics
        latency_ms = int((time.time() - start_time) * 1000)
        metric = Metric(
            session_id=session_id,
            query=query,
            latency_ms=latency_ms,
            chunks_retrieved=len(context_chunks),
            model_used=model_name
        )
        db.add(metric)
        await db.commit()
        
        return {
            "response": answer,
            "context": context_chunks
        }

# Singleton instance
llm_service = LLMService()
