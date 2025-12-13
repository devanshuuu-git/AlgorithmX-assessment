from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    AsyncEngine,
)
from sqlalchemy.orm import sessionmaker

from app.config import settings
from app.db.models import Base

DATABASE_URL = (
    f"postgresql+asyncpg://{settings.POSTGRES_USER}:"
    f"{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:"
    f"{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
)

# 🔹 Global async engine
engine: AsyncEngine = create_async_engine(
    DATABASE_URL,
    echo=False,
)

# 🔹 Session factory
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# 🔹 Dependency (optional for future use)
async def get_db():
    async with async_session() as session:
        yield session

# 🔹 Initialize DB (create tables)
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
