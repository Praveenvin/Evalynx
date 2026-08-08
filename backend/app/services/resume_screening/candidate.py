from dataclasses import dataclass, field

from app.services.rag.chunker import DocumentChunk


@dataclass
class Candidate:
    candidate_id: str
    filename: str

    resume_text: str = ""

    chunks: list[DocumentChunk] = field(
        default_factory=list
    )

    retrieved_evidence: list[dict] = field(
        default_factory=list
    )