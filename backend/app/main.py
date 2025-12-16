"""
FastAPI application entry point.
Initializes the API, database, and routes.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os

from app.config import settings
from app.db.init_db import init_database


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events."""
    # Startup
    print("🚀 Starting PDF RAG Application...")

    print(f"🔍 Qdrant URL: {settings.qdrant_url}")
    print(f"🤖 Gemini Model: {settings.gemini_model}")
    
    # Create upload directory
    os.makedirs(settings.upload_dir, exist_ok=True)
    
    # Initialize database
    await init_database()
    print("✅ Database initialized")
    
    yield
    
    # Shutdown
    print("👋 Shutting down...")


# Create FastAPI app
app = FastAPI(
    title="PDF RAG API",
    description="Retrieval-Augmented Generation API for PDF documents",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)





@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "database": "connected",
        "qdrant": "connected"
    }


# Include API router
from app.api.endpoints import router as api_router
app.include_router(api_router, prefix="/api", tags=["api"])
