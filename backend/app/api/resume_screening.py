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
    db: Session = Depends(get_db),
):
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