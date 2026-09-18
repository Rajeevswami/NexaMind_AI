from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PayloadSchemaType
from app.core.config import settings
from app.rag.embeddings import EMBEDDING_DIM
client = QdrantClient(url=settings.qdrant_url, api_key=settings.qdrant_api_key)
COLLECTION = settings.qdrant_collection
def ensure_collection() -> None:
    if not client.collection_exists(COLLECTION):
        client.create_collection(COLLECTION, vectors_config=VectorParams(size=EMBEDDING_DIM, distance=Distance.COSINE))
    for field in ("user_id", "document_id"):
        client.create_payload_index(COLLECTION, field, PayloadSchemaType.INTEGER)

