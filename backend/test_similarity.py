from app.services.rag.document_loader import extract_text
from app.services.rag.chunker import create_chunks
from app.services.rag.similarity import rank_chunks_by_similarity


file_path = "data/atsresume.pdf"

resume_text = extract_text(file_path)

chunks = create_chunks(resume_text)

job_description = """
We are looking for a Software Developer with strong experience
in React, TypeScript, Python, FastAPI, REST APIs and PostgreSQL.
The candidate should have experience building full-stack web
applications and integrating frontend applications with backend APIs.
"""

results = rank_chunks_by_similarity(
    query=job_description,
    chunks=chunks,
    top_k=5,
)

print("\nMost relevant resume sections:\n")

for result in results:
    print("=" * 70)
    print(f"Chunk ID : {result['chunk_id']}")
    print(f"Section  : {result['section']}")
    print(f"Score    : {result['score']:.4f}")
    print("=" * 70)
    print(result["text"][:500])
    print()