from app.services.resume_screening.batch_screening import (
    BatchScreeningService,
)


job_description = """
We are looking for a Software Developer with strong
experience in React, TypeScript, Python, FastAPI,
REST APIs and PostgreSQL.

The candidate should have experience building
full-stack web applications, integrating frontend
applications with backend APIs, and working with
relational databases.

Candidates with strong software development,
problem-solving and API integration experience
are preferred.
"""


service = BatchScreeningService()

results = service.screen_directory(
    directory="data/resumes",
    job_description=job_description,
    top_k=5,
)


print("\n")
print("=" * 80)
print("FINAL CANDIDATE RANKING")
print("=" * 80)

for rank, result in enumerate(
    results,
    start=1,
):
    print(
        f"\n#{rank} "
        f"{result['filename']}"
    )

    print(
        f"Overall Score: "
        f"{result['overall_score']}/100"
    )

    print(
        f"Skills: "
        f"{result['skills_score']}/100"
    )

    print(
        f"Experience: "
        f"{result['experience_score']}/100"
    )

    print(
        f"Education: "
        f"{result['education_score']}/100"
    )

    print(
        f"Recommendation: "
        f"{result['recommendation']}"
    )

    print(
        f"Strengths: "
        f"{result['strengths']}"
    )

    print(
        f"Gaps: "
        f"{result['gaps']}"
    )
    print(
        f"Semantic: "
        f"{result['semantic_score']:.2f}"
    )