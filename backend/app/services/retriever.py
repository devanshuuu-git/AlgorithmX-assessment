from qdrant_client import QdrantClient
from qdrant_client.http import models as qmodels
from langchain_qdrant import QdrantVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from app.config import settings

COLLECTION_NAME = "rag_collection"


def get_embedding():
    return GoogleGenerativeAIEmbeddings(
        model=settings.EMBEDDING_MODEL,
        google_api_key=settings.GEMINI_API_KEY,
    )


def get_qdrant_client():
    return QdrantClient(
        host=settings.QDRANT_HOST,
        port=settings.QDRANT_PORT,
        check_compatibility=False,
    )


def ensure_collection(client: QdrantClient, vector_size: int):
    try:
        client.get_collection(COLLECTION_NAME)
    except Exception:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=qmodels.VectorParams(
                size=vector_size,
                distance=qmodels.Distance.COSINE,
            ),
        )


def get_vector_store():
    embedding = get_embedding()
    client = get_qdrant_client()

    # ✅ MUST come BEFORE QdrantVectorStore()
    ensure_collection(client, vector_size=768)

    return QdrantVectorStore(
        client=client,
        collection_name=COLLECTION_NAME,
        embedding=embedding,
    )

async def retrieve_context(
    query: str,
    top_k: int = 5,
    doc_filter: list[str] | None = None,
):
    vector_store = get_vector_store()

    qdrant_filter = None
    if doc_filter:
        qdrant_filter = qmodels.Filter(
            must=[
                qmodels.FieldCondition(
                    key="doc_name",
                    match=qmodels.MatchAny(any=doc_filter),
                )
            ]
        )

    docs = vector_store.similarity_search(
        query=query,
        k=top_k,
        filter=qdrant_filter,
    )

    return [
        {
            "text": doc.page_content,
            "page": doc.metadata.get("page"),
            "doc": doc.metadata.get("doc_name"),
        }
        for doc in docs
    ]
