from pydantic import BaseModel

class IngestResponse(BaseModel):
    status: str
    chunks_indexed: int
