
from app.db.session import engine, Base
from app.models.models import User, Session, Document, Message, Metric


async def init_database():
    """Initialize database tables."""
    try:
        async with engine.begin() as conn:
            # Create all tables
            await conn.run_sync(Base.metadata.create_all)
        print("✅ Database tables created successfully")
    except Exception as e:
        print(f"❌ Error creating database tables: {e}")
        raise
