from app.db.session import async_session
from app.db.models import ChatMessage

async def save_chat_message(session_id, question, answer, retrieved, model_used):
    async with async_session() as db:
        msg = ChatMessage(
            session_id=session_id,
            question=question,
            answer=answer,
            retrieved=retrieved,
            model_used=model_used,
        )
        db.add(msg)
        await db.commit()
