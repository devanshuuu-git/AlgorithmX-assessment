from fastapi import APIRouter, UploadFile, HTTPException
from app.services.pdf_ingest import ingest_pdf_file

router = APIRouter()

@router.post("/")
async def ingest_pdf(file: UploadFile):

    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    chunks_count = await ingest_pdf_file(file)

    return {
        "status": "success",
        "file": file.filename,
        "chunks_indexed": chunks_count
    }
