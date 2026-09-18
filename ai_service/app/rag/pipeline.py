import uuid
from qdrant_client.models import Filter, FieldCondition, MatchValue, PointStruct
from app.rag.embeddings import embed_batch
from app.rag.loaders import load_document
from app.rag.qdrant_client import COLLECTION, client, ensure_collection
from app.rag.retriever import search_chunks
from app.rag.text_splitter import split_into_chunks
def ingest_document(file_path: str, file_type: str, document_id: int, user_id: int) -> int:
    ensure_collection()
    client.delete(COLLECTION, points_selector=Filter(must=[FieldCondition(key="user_id", match=MatchValue(value=user_id)), FieldCondition(key="document_id", match=MatchValue(value=document_id))]))
    chunks = split_into_chunks(load_document(file_path, file_type))
    if not chunks: return 0
    vectors = embed_batch([chunk.text for chunk in chunks])
    client.upsert(COLLECTION, points=[PointStruct(id=str(uuid.uuid4()), vector=vector, payload={"user_id":user_id,"document_id":document_id,"page_number":chunk.page_number,"chunk_index":chunk.chunk_index,"text":chunk.text}) for chunk, vector in zip(chunks, vectors)])
    return len(chunks)
def build_context(question: str, user_id: int, document_id: int | None = None) -> tuple[str, list[dict]]:
    sources = search_chunks(question, user_id, document_id)
    return "\n\n---\n\n".join(f"[Document {s['document_id']}, page {s['page_number']}]\n{s['text']}" for s in sources), sources
