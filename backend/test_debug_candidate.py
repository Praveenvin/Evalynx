from app.services.resume_screening.resume_processor import (
    process_resume,
)
from app.services.resume_screening.retriever import (
    CandidateRetriever,
)


candidate = process_resume(
    "data/resumes/student1.pdf"
)

print("\nCandidate:")
print(candidate.filename)

print("\nTotal chunks:")
print(len(candidate.chunks))

print("\nAll sections:")
for chunk in candidate.chunks:
    print(
        f"Chunk {chunk.chunk_id} | "
        f"{chunk.section} | "
        f"{len(chunk.text)} characters"
    )


job_description = """
We are looking for a Software Developer with strong
experience in React, TypeScript, Python, FastAPI,
REST APIs and PostgreSQL.

The candidate should have experience building
full-stack web applications, integrating frontend
applications with backend APIs, and working with
relational databases.
"""


retriever = CandidateRetriever()

results = retriever.retrieve(
    candidate=candidate,
    job_description=job_description,
    top_k=5,
)

print("\n")
print("=" * 80)
print("RETRIEVED EVIDENCE")
print("=" * 80)

for result in results:
    print("\n" + "=" * 80)
    print(
        f"Chunk: {result['chunk_id']}"
    )
    print(
        f"Section: {result['section']}"
    )
    print(
        f"Score: {result['score']:.4f}"
    )
    print("-" * 80)
    print(result["text"])