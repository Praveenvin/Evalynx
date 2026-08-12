from pathlib import Path
import shutil
import tempfile
from typing import Annotated

from fastapi import (
    APIRouter,
    File,
    Form,
    HTTPException,
    UploadFile,
    Depends,
)
from sqlalchemy.orm import Session

from app.core.database import get_db

from app.services.resume_screening.batch_screening import (
    BatchScreeningService,
)
from app.services.llm.groq_client import GroqServiceError


router = APIRouter(
    prefix="/api/resume-screening",
    tags=["Resume Screening"],
)


@router.post("/screen")
async def screen_resumes(
    job_description: Annotated[
        str,
        Form(),
    ],
    resumes: Annotated[
        list[UploadFile],
        File(),
    ],
    groq_api_key: Annotated[
        str | None,
        Form(),
    ] = None,
    api_provider: Annotated[
        str,
        Form(),
    ] = "evalynx",
    db: Session = Depends(get_db),
):
    if api_provider == "user" and (not groq_api_key or not groq_api_key.strip()):
        raise GroqServiceError("Please enter your Groq API key.", code="MISSING_API_KEY")

    if not resumes:
        raise HTTPException(
            status_code=400,
            detail="At least one resume is required.",
        )

    service = BatchScreeningService()

    temp_dir = Path(
        tempfile.mkdtemp(
            prefix="evalynx_resumes_"
        )
    )

    try:
        for resume in resumes:
            if not resume.filename:
                continue

            file_path = temp_dir / resume.filename

            with file_path.open("wb") as buffer:
                shutil.copyfileobj(
                    resume.file,
                    buffer,
                )

        results = service.screen_directory(
            db=db,
            directory=str(temp_dir),
            job_description=job_description,
            top_k=5,
            api_provider=api_provider,
            api_key=groq_api_key,
        )

        return {
            "total_candidates": len(results),
            "results": results,
        }

    finally:
        shutil.rmtree(
            temp_dir,
            ignore_errors=True,
        )

from app.schemas import PaginatedResponse, ResumeScreeningHistoryItem
from app.models.resume_screening import ResumeScreeningModel

@router.get("/history", response_model=PaginatedResponse[ResumeScreeningHistoryItem])
async def get_history(page: int = 1, page_size: int = 10, db: Session = Depends(get_db)):
    offset = (page - 1) * page_size
    total = db.query(ResumeScreeningModel).count()
    items = db.query(ResumeScreeningModel).order_by(ResumeScreeningModel.created_at.desc()).offset(offset).limit(page_size).all()
    
    response_items = []
    for item in items:
        candidates = item.candidates
        top_score = max((c.overall_score for c in candidates), default=None) if candidates else None
        response_items.append({
            "id": item.id,
            "created_at": item.created_at,
            "job_description": item.job_description[:100] + "..." if len(item.job_description) > 100 else item.job_description,
            "candidate_count": len(candidates),
            "top_score": top_score,
            "status": item.status
        })
        
    return {
        "items": response_items,
        "page": page,
        "page_size": page_size,
        "total": total,
        "total_pages": (total + page_size - 1) // page_size
    }

@router.get("/history/{id}")
async def get_history_detail(id: str, db: Session = Depends(get_db)):
    item = db.query(ResumeScreeningModel).filter(ResumeScreeningModel.id == id).first()
    if not item:
        raise HTTPException(404, "History not found")
        
    results = []
    for c in item.candidates:
        evidence = [{"text": e.text, "similarity_score": e.similarity_score} for e in c.evidence]
        results.append({
            "filename": c.filename,
            "candidate_name": c.candidate_name,
            "email": c.email,
            "overall_score": c.overall_score,
            "skills_score": c.skills_score,
            "experience_score": c.experience_score,
            "education_score": c.education_score,
            "semantic_score": c.semantic_score,
            "strengths": c.strengths,
            "gaps": c.gaps,
            "recommendation": c.recommendation,
            "rank": c.rank,
            "evidence": evidence
        })
        
    return {
        "id": item.id,
        "created_at": item.created_at,
        "job_description": item.job_description,
        "status": item.status,
        "total_candidates": len(results),
        "results": results
    }