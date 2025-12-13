from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.routes import ingest, chat
from app.db.session import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 🔹 Startup
    await init_db()
    yield
    # 🔹 Shutdown (optional cleanup later)


app = FastAPI(
    title="AlgorithmX RAG Backend",
    version="1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ingest.router, prefix="/ingest", tags=["Ingest"])
app.include_router(chat.router, prefix="/chat", tags=["Chat"])


@app.get("/")
async def root():
    return {"status": "running"}
