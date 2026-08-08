from pathlib import Path

from app.services.rag.chunker import create_chunks
from app.services.rag.document_loader import extract_text
from app.services.resume_screening.candidate import Candidate


SUPPORTED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".txt",
}


def process_resume(
    file_path: str,
) -> Candidate:

    path = Path(file_path)

    if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            f"Unsupported resume format: {path.suffix}"
        )

    resume_text = extract_text(
        str(path)
    )

    chunks = create_chunks(
        resume_text
    )

    return Candidate(
        candidate_id=path.stem,
        filename=path.name,
        resume_text=resume_text,
        chunks=chunks,
    )