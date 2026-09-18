from dataclasses import dataclass
from pathlib import Path
import fitz
from docx import Document as DocxDocument

@dataclass(frozen=True)
class ExtractedPage:
    page_number: int
    text: str

def load_pdf(file_path: str) -> list[ExtractedPage]:
    with fitz.open(file_path) as document:
        return [ExtractedPage(index, page.get_text().strip()) for index, page in enumerate(document, 1) if page.get_text().strip()]

def load_docx(file_path: str) -> list[ExtractedPage]:
    paragraphs = [paragraph.text.strip() for paragraph in DocxDocument(file_path).paragraphs if paragraph.text.strip()]
    return [ExtractedPage(index // 40 + 1, "\n".join(paragraphs[index:index + 40])) for index in range(0, len(paragraphs), 40)]

def load_txt(file_path: str) -> list[ExtractedPage]:
    text = Path(file_path).read_text(encoding="utf-8", errors="replace").strip()
    return [ExtractedPage(1, text)] if text else []

def load_document(file_path: str, file_type: str) -> list[ExtractedPage]:
    loaders = {"pdf": load_pdf, "docx": load_docx, "txt": load_txt}
    if file_type not in loaders: raise ValueError("Unsupported document type")
    return loaders[file_type](file_path)

