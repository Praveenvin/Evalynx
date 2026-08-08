from pathlib import Path
from app.services.rag.text_cleaner import clean_text
import pymupdf  # PyMuPDF
from docx import Document


def extract_pdf_text(file_path: str) -> str:
    """Extract text from a PDF file."""
    text = []

    with pymupdf.open(file_path) as pdf:
        for page in pdf:
            page_text = page.get_text()
            if page_text:
                text.append(page_text)

    return "\n".join(text).strip()


def extract_docx_text(file_path: str) -> str:
    """Extract text from a DOCX file."""
    document = Document(file_path)

    paragraphs = [
        paragraph.text.strip()
        for paragraph in document.paragraphs
        if paragraph.text.strip()
    ]

    return "\n".join(paragraphs).strip()


def extract_text(file_path: str) -> str:
    """Extract and clean text based on the file extension."""
    path = Path(file_path)

    if path.suffix.lower() == ".pdf":
        text = extract_pdf_text(file_path)

    elif path.suffix.lower() == ".docx":
        text = extract_docx_text(file_path)

    elif path.suffix.lower() == ".txt":
        text = path.read_text(encoding="utf-8")

    else:
        raise ValueError(
            f"Unsupported file type: {path.suffix}. "
            "Supported formats: PDF, DOCX, TXT."
        )

    return clean_text(text)