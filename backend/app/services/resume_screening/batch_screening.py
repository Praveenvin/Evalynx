from pathlib import Path

from app.services.resume_screening.resume_processor import (
    process_resume,
)
from app.services.resume_screening.retriever import (
    CandidateRetriever,
)
from app.services.llm.groq_service import groq_service

from app.services.resume_screening.scoring import (
    calculate_final_score,
)

SUPPORTED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".txt",
}


class BatchScreeningService:
    def __init__(self):
        self.retriever = CandidateRetriever()

    def screen_directory(
        self,
        directory: str,
        job_description: str,
        top_k: int = 5,
        api_key: str | None = None,
    ) -> list[dict]:

        directory_path = Path(directory)

        resume_files = sorted(
            [
                file
                for file in directory_path.iterdir()
                if file.is_file()
                and file.suffix.lower()
                in SUPPORTED_EXTENSIONS
            ]
        )

        results = []

        for file_path in resume_files:
            print(
                f"Processing: {file_path.name}"
            )

            try:
                candidate = process_resume(
                    str(file_path)
                )

                evidence = self.retriever.retrieve(
                    candidate=candidate,
                    job_description=job_description,
                    top_k=top_k,
                )

                evaluation = (
                    groq_service.evaluate_candidate(
                        job_description=job_description,
                        evidence=evidence,
                        api_key=api_key,
                    )
                )

                scored_result = calculate_final_score(
                    llm_evaluation=evaluation,
                    retrieved_evidence=evidence,
                )

                result = {
                    "candidate_id": candidate.candidate_id,
                    "filename": candidate.filename,
                    **scored_result,
                }

                results.append(result)

            except Exception as error:
                print(
                    f"Failed: {file_path.name}"
                )
                print(f"Error: {error}")

        results.sort(
            key=lambda item: item["overall_score"],
            reverse=True,
        )

        return results