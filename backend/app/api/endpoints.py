from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from typing import List
import shutil
import os
import uuid

from app.db.session import get_db
from app.models.models import User, Session, Document, Message
from app.schemas import ChatRequest, ChatResponse, SessionResponse, MessageResponse, DocumentResponse
from app.services.indexing_service import indexing_service

from app.services.llm_service import llm_service

router = APIRouter()
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# --- Document Management ---

@router.post("/upload", response_model=DocumentResponse)
async def upload_document(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    """Upload and index a PDF document."""
    file_id = str(uuid.uuid4())
    file_ext = os.path.splitext(file.filename)[1]
    saved_filename = f"{file_id}{file_ext}"
    file_path = os.path.join(UPLOAD_DIR, saved_filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    new_doc = Document(
        filename=file.filename,
        file_hash=file_id, 
        status="indexing"
    )
    db.add(new_doc)
    await db.commit()
    await db.refresh(new_doc)
    
    try:
        await indexing_service.index_file(file_path)
        new_doc.status = "indexed"
        await db.commit()
    except Exception as e:
        new_doc.status = "error"
        await db.commit()
        raise HTTPException(status_code=500, detail=f"Indexing failed: {str(e)}")
        
    return new_doc

@router.get("/documents", response_model=List[DocumentResponse])
async def list_documents(db: AsyncSession = Depends(get_db)):
    """List all uploaded documents."""
    result = await db.execute(select(Document).order_by(desc(Document.created_at)))
    return result.scalars().all()

# --- Chat & Session Management ---

@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    db: AsyncSession = Depends(get_db)
):
    """Send a query to the RAG system."""
    # 1. Get or Create Session
    if not request.session_id:
        result = await db.execute(select(User).where(User.id == 1))
        user = result.scalar_one_or_none()
        if not user:
            user = User(id=1)
            db.add(user)
            await db.commit()
            
        new_session = Session(user_id=1, title=request.query[:30] + "...")
        db.add(new_session)
        await db.commit()
        await db.refresh(new_session)
        session_id = new_session.id
    else:
        session_id = request.session_id
        
    # 2. Save User Message
    user_msg = Message(
        session_id=session_id,
        role="user",
        content=request.query
    )
    db.add(user_msg)
    await db.commit()
    
    # 3. Get Response from LLM Service (with new params)
    try:
        result = await llm_service.generate_response(
            query=request.query,
            session_id=session_id,
            db=db,
            model_name=request.model_name,
            top_k=request.top_k,
            doc_filter=request.doc_filter
        )
        response_text = result["response"]
        context_chunks = result["context"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"RAG generation failed: {str(e)}")
    
    # 4. Save Assistant Message
    ai_msg = Message(
        session_id=session_id,
        role="assistant",
        content=response_text
    )
    db.add(ai_msg)
    await db.commit()
    
    return ChatResponse(
        response=response_text,
        session_id=session_id,
        citations=[], 
        context=context_chunks # Return context for UI
    )

@router.get("/sessions", response_model=List[SessionResponse])
async def list_sessions(db: AsyncSession = Depends(get_db)):
    """List all chat sessions."""
    result = await db.execute(
        select(Session).where(Session.user_id == 1).order_by(desc(Session.updated_at))
    )
    return result.scalars().all()

@router.get("/sessions/{session_id}/messages", response_model=List[MessageResponse])
async def get_session_messages(
    session_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get message history for a session."""
    result = await db.execute(
        select(Message).where(Message.session_id == session_id).order_by(Message.created_at)
    )
    return result.scalars().all()

@router.post("/sessions", response_model=SessionResponse)
async def create_session(db: AsyncSession = Depends(get_db)):
    """Create a new empty session."""
    result = await db.execute(select(User).where(User.id == 1))
    user = result.scalar_one_or_none()
    if not user:
        user = User(id=1)
        db.add(user)
        await db.commit()
        
    new_session = Session(user_id=1, title="New Chat")
    db.add(new_session)
    await db.commit()
    await db.refresh(new_session)
    return new_session
