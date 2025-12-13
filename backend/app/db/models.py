from sqlalchemy import Column, Integer, String, JSON, TIMESTAMP, text
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True)
    session_id = Column(String)
    question = Column(String)
    answer = Column(String)
    retrieved = Column(JSON)
    model_used = Column(String)
    timestamp = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
