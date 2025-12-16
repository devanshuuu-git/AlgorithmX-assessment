from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Gemini API
    gemini_api_key: str
    gemini_model: str = "gemini-2.5-flash"
    
    # Embedding Model (using Gemini)
    embedding_model: str = "models/embedding-001"
    
    # PostgreSQL
    postgres_user: str = "postgres"
    postgres_password: str = "postgres"
    postgres_db: str = "rag_db"
    postgres_host: str = "postgres"
    postgres_port: int = 5432
    
    # Qdrant
    qdrant_url: str = "http://qdrant:6333"
    qdrant_collection_name: str = "pdf_documents"
    
    # Application
    upload_dir: str = "/app/uploads"
    chunk_size: int = 1000
    chunk_overlap: int = 300
    default_top_k: int = 4
    
    class Config:
        env_file = ".env"
        case_sensitive = False
    
    @property
    def database_url(self) -> str:
        """Construct async PostgreSQL connection URL."""
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )


# Global settings instance
settings = Settings()
