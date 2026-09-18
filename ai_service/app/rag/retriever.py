from qdrant_client.models import FieldCondition, Filter, MatchValue
from app.rag.embeddings import embed_text
from app.rag.qdrant_client import COLLECTION, client
def search_chunks(query: str, user_id: int, document_id: int | None = None) -> list[dict]:
    conditions = [FieldCondition(key="user_id", match=MatchValue(value=user_id))]
    if document_id is not None: conditions.append(FieldCondition(key="document_id", match=MatchValue(value=document_id)))
    results = client.search(collection_name=COLLECTION, query_vector=embed_text(query), query_filter=Filter(must=conditions), limit=5)
    return [{"text": h.payload["text"], "document_id": h.payload["document_id"], "page_number": h.payload["page_number"], "score": h.score} for h in results]

