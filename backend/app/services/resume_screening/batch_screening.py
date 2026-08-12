from pathlib import Path

from app.services.resume_screening.resume_processor import (
    process_resume,
)
from app.services.resume_screening.retriever import (
    CandidateRetriever,
)
from app.services.llm.groq_service import groq_service
from app.services.llm.groq_client import GroqServiceError

from sqlalchemy.orm import Session

from app.services.resume_screening.scoring import (
    calculate_final_score,
)

from app.models.resume_screening import (
    ResumeScreeningModel,
    ResumeCandidateModel,
    ResumeEvidenceModel,
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
        db: Session,
        directory: str,
        job_description: str,
        top_k: int = 5,
        api_provider: str = "evalynx",
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

        screening = ResumeScreeningModel(
            job_description=job_description,
            status="processing",
        )
        db.add(screening)
        db.commit()
        db.refresh(screening)

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
                        api_provider=api_provider,
                        api_key=api_key,
                    )
                )

                scored_result = calculate_final_score(
                    llm_evaluation=evaluation,
                    retrieved_evidence=evidence,
                )

                candidate_record = ResumeCandidateModel(
                    screening_id=screening.id,
                    filename=candidate.filename,
                    candidate_name=None,
                    email=None,
                    overall_score=scored_result["overall_score"],
                    skills_score=scored_result["skills_score"],
                    experience_score=scored_result["experience_score"],
                    education_score=scored_result["education_score"],
                    semantic_score=scored_result["semantic_score"],
                    strengths=scored_result["strengths"],
                    gaps=scored_result["gaps"],
                    recommendation=scored_result["recommendation"],
                )
                db.add(candidate_record)
                db.flush()

                for ev in evidence:
                    evidence_record = ResumeEvidenceModel(
                        candidate_id=candidate_record.id,
                        text=ev.get("text", ""),
                        similarity_score=ev.get("score", 0.0),
                    )
                    db.add(evidence_record)

                db.commit()

                result = {
                    "candidate_id": candidate_record.id,
                    "filename": candidate.filename,
                    **scored_result,
                }

                results.append(result)

            except GroqServiceError:
                db.rollback()
                raise
            except Exception as error:
                db.rollback()
                print(
                    f"Failed: {file_path.name}"
                )
                print(f"Error: {error}")

        results.sort(
            key=lambda item: item["overall_score"],
            reverse=True,
        )

        for index, item in enumerate(results):
            rank = index + 1
            item["rank"] = rank
            db.query(ResumeCandidateModel).filter_by(id=item["candidate_id"]).update({"rank": rank})
            
        screening.status = "completed"
        db.commit()

        return results