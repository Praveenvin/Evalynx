from app.services.rag.document_loader import extract_text
from app.services.rag.chunker import create_chunks
from app.services.rag.embeddings import embedding_service
from app.services.rag.vector_store import FAISSVectorStore


file_path = "data/atsresume.pdf"

resume_text = extract_text(file_path)
chunks = create_chunks(resume_text)

chunk_texts = [chunk.text for chunk in chunks]

embeddings = embedding_service.encode(chunk_texts)

metadata = [
    {
        "chunk_id": chunk.chunk_id,
        "section": chunk.section,
        "text": chunk.text,
    }
    for chunk in chunks
]

dimension = embeddings.shape[1]

vector_store = FAISSVectorStore(
    dimension=dimension,
)

vector_store.add(
    embeddings,
    metadata,
)

print(f"Indexed chunks: {vector_store.size}")

job_description = """
We are looking for a Software Developer with strong experience
in React, TypeScript, Python, FastAPI, REST APIs and PostgreSQL.
The candidate should have experience building full-stack web
applications and integrating frontend applications with backend APIs.
"""

query_embedding = embedding_service.encode(
    [job_description]
)[0]

results = vector_store.search(
    query_embedding,
    top_k=5,
)

print("\nTop retrieved chunks:\n")

for result in results:
    print("=" * 70)
    print(f"Chunk   : {result['chunk_id']}")
    print(f"Section : {result['section']}")
    print(f"Score   : {result['score']:.4f}")
    print("=" * 70)
    print(result["text"][:500])
    print()