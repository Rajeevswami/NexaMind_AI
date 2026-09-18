from sentence_transformers import SentenceTransformer
EMBEDDING_DIM = 384
_model: SentenceTransformer | None = None
def _get_model() -> SentenceTransformer:
    global _model
    if _model is None: _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model
def embed_text(text: str) -> list[float]: return _get_model().encode(text, normalize_embeddings=True).tolist()
def embed_batch(texts: list[str]) -> list[list[float]]: return _get_model().encode(texts, normalize_embeddings=True, batch_size=32).tolist()

