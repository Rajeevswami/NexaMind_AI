from typing import Literal
from pydantic import BaseModel, Field
class DocumentProcessRequest(BaseModel):
    document_id: int = Field(gt=0); user_id: int = Field(gt=0); file_path: str = Field(min_length=1); file_type: Literal["pdf", "docx", "txt"]
class DocumentProcessResponse(BaseModel): document_id: int; chunks_stored: int; status: str
class DocumentSearchRequest(BaseModel): user_id: int = Field(gt=0); query: str = Field(min_length=1); document_id: int | None = Field(default=None, gt=0)
class SourceChunk(BaseModel): document_id: int; page_number: int; text: str; score: float
class DocumentSearchResponse(BaseModel): results: list[SourceChunk]
