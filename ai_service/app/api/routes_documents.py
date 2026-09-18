import logging
from fastapi import APIRouter, Depends, HTTPException
from app.core.security import verify_internal_key
from app.rag.pipeline import build_context, ingest_document
from app.schemas.documents import DocumentProcessRequest, DocumentProcessResponse, DocumentSearchRequest, DocumentSearchResponse, SourceChunk
logger = logging.getLogger(__name__)
router = APIRouter(prefix="/ai", tags=["documents"], dependencies=[Depends(verify_internal_key)])
@router.post("/documents/process", response_model=DocumentProcessResponse)
async def process_document(payload: DocumentProcessRequest):
    try: count = ingest_document(payload.file_path, payload.file_type, payload.document_id, payload.user_id)
    except Exception as error:
        logger.exception("Document processing failed document_id=%s", payload.document_id)
        raise HTTPException(500, "Document processing failed") from error
    return DocumentProcessResponse(document_id=payload.document_id, chunks_stored=count, status="ready" if count else "no_extractable_text")
@router.post("/documents/search", response_model=DocumentSearchResponse)
async def search_documents(payload: DocumentSearchRequest):
    _, sources = build_context(payload.query, payload.user_id, payload.document_id)
    return DocumentSearchResponse(results=[SourceChunk(**source) for source in sources])
