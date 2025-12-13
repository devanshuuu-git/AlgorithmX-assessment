from fastapi import APIRouter
from app.schemas.chat import ChatRequest
from app.services.retriever import retrieve_context
from app.services.llm import generate_answer
from app.db.crud import save_chat_message
from app.services.retriever import retrieve_context

router = APIRouter()

@router.post("/")
async def chat(payload: ChatRequest):

    # Retrieve documents
    contexts = await retrieve_context(
        query=payload.query,
        top_k=payload.top_k,
        doc_filter=payload.doc_filter
    )

    # Enforce “only answer if sources found”
    if payload.only_if_sources and len(contexts) == 0:
        return {
            "answer": "No relevant sources found. Cannot answer.",
            "sources": []
        }

    # LLM Answer
    answer = await generate_answer(
        query=payload.query,
        contexts=contexts,
        model=payload.model
    )

    # Save chat message in database
    await save_chat_message(
        session_id=payload.session_id,
        question=payload.query,
        answer=answer["answer"],
        retrieved=contexts,
        model_used=payload.model,
    )

    return answer
