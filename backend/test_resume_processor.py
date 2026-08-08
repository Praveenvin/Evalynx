from app.services.resume_screening.resume_processor import (
    process_resume,
)


file_path = "data/atsresume.pdf"

candidate = process_resume(
    file_path
)

print("\nCandidate")
print("=" * 50)

print("ID:", candidate.candidate_id)
print("Filename:", candidate.filename)

print(
    "Text length:",
    len(candidate.resume_text),
)

print(
    "Chunks:",
    len(candidate.chunks),
)

print("\nSections:")

for chunk in candidate.chunks:
    print(
        f"- {chunk.section}"
    )