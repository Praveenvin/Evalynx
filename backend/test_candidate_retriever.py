from app.services.resume_screening.resume_processor import (
    process_resume,
)

from app.services.resume_screening.retriever import (
    CandidateRetriever,
)


candidate = process_resume(
    "data/atsresume.pdf"
)

job_description = """
We are looking for a Software Developer with strong
experience in React, TypeScript, Python, FastAPI,
REST APIs and PostgreSQL.

The candidate should have experience building
full-stack web applications and integrating
frontend applications with backend APIs.
"""

retriever = CandidateRetriever()

results = retriever.retrieve(
    candidate=candidate,
    job_description=job_description,
    top_k=5,
)

print("\nRetrieved evidence")
print("=" * 70)

for result in results:
    print(
        f"Section: {result['section']}"
    )

    print(
        f"Score: {result['score']:.4f}"
    )

    print(
        f"Candidate: {result['candidate_id']}"
    )

    print("-" * 70)

    print(
        result["text"][:400]
    )

    print()