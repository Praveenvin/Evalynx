"""
Minimal PDF text extraction for resume-based interviews.

This is a lightweight fallback for Mock Interview.
The Resume Screening pipeline can still be used separately for
advanced resume processing such as chunking and embeddings.
"""

import io

from pypdf import PdfReader


def extract_resume_text(file_bytes: bytes) -> str:
    """Extract plain text from a PDF resume."""

    try:
        reader = PdfReader(io.BytesIO(file_bytes))

        pages = [
            page.extract_text() or ""
            for page in reader.pages
        ]

        text = "\n".join(pages).strip()

        if not text:
            raise ValueError(
                "No readable text found in the resume PDF."
            )

        return text

    except Exception as exc:
        raise ValueError(
            f"Could not read resume PDF: {exc}"
        ) from exc