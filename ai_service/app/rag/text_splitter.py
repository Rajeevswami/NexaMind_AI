from dataclasses import dataclass
from app.rag.loaders import ExtractedPage

CHUNK_SIZE, CHUNK_OVERLAP = 800, 150
@dataclass(frozen=True)
class Chunk:
    text: str; page_number: int; chunk_index: int

def split_into_chunks(pages: list[ExtractedPage]) -> list[Chunk]:
    chunks, index = [], 0
    for page in pages:
        for start in range(0, len(page.text), CHUNK_SIZE - CHUNK_OVERLAP):
            text = page.text[start:start + CHUNK_SIZE].strip()
            if text:
                chunks.append(Chunk(text, page.page_number, index)); index += 1
    return chunks

