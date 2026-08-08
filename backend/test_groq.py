from app.services.llm.groq_service import (
    groq_service,
)


job_description = """
We are looking for a Software Developer with strong
experience in React, TypeScript, Python, FastAPI,
REST APIs and PostgreSQL.

The candidate should have experience building
full-stack web applications.
"""


evidence = [
    {
        "section": "SKILLS",
        "text": """
        Python, TypeScript, React, FastAPI,
        PostgreSQL, REST APIs
        """,
    },
    {
        "section": "EXPERIENCE",
        "text": """
        Developed full-stack applications using React,
        TypeScript, Django and PostgreSQL.
        Integrated frontend applications with backend
        REST APIs.
        """,
    },
]


result = groq_service.evaluate_candidate(
    job_description=job_description,
    evidence=evidence,
)


print("\nCandidate Evaluation")
print("=" * 60)

for key, value in result.items():
    print(f"{key}: {value}")