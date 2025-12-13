import tempfile
from langchain_community.document_loaders import PyPDFLoader
from app.utils.text_splitter import get_text_splitter
from app.services.retriever import get_vector_store

async def ingest_pdf_file(file):

    # Save file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(await file.read())
        temp_path = tmp.name

    # Load PDF into LangChain Documents
    loader = PyPDFLoader(temp_path)
    documents = loader.load()      # extracts per-page content

    # Apply text splitter
    splitter = get_text_splitter()
    chunks = splitter.split_documents(documents)

    # Add metadata consistently
    for idx, chunk in enumerate(chunks):
        chunk.metadata["doc_name"] = file.filename
        chunk.metadata["chunk_index"] = idx

    # Store in Qdrant via LangChain
    vector_store = get_vector_store()
    vector_store.add_documents(chunks)

    return len(chunks)
