import json
import logging

from fastapi import APIRouter, File, Form, HTTPException, UploadFile, Depends
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas import (
    AnswerRequest,
    AnswerResponse,
    ReplayQuestionResponse,
    SpeakRequest,
    StartInterviewResponse,
    VoiceAnswerResponse,
)

from app.services.llm.groq_client import GroqServiceError

from app.services.mock_interview.interview_service import (
    InterviewCompleteError,
    InterviewNotFoundError,
    build_final_evaluation,
    start_interview,
    submit_answer,
    get_session_auth,
)

from app.services.llm.speech_service import (
    synthesize_speech,
    transcribe_audio,
)

from app.services.mock_interview.resume_extractor import (
    extract_resume_text,
)

from app.services.mock_interview.session_store import (
    get_session,
    save_session,
)


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/mock-interview",
    tags=["Mock Interview"],
)


@router.post(
    "/start",
    response_model=StartInterviewResponse,
)
async def start(
    source: str = Form(...),
    role: str = Form(""),
    skills: str = Form("[]"),
    mode: str = Form(...),
    duration: int = Form(...),
    question_count: int = Form(...),
    resume: UploadFile | None = File(None),
    api_provider: str = Form("evalynx"),
    groq_api_key: str | None = Form(None),
    security_mode: str = Form("standard"),
    db: Session = Depends(get_db),
):
    if api_provider == "user" and (not groq_api_key or not groq_api_key.strip()):
        raise GroqServiceError("Please enter your Groq API key.", code="MISSING_API_KEY")
    """
    Start a mock interview.

    Uses multipart/form-data so a resume PDF can be uploaded
    when source is 'resume'.
    """

    try:
        parsed_skills = json.loads(skills) if skills else []

        if not isinstance(parsed_skills, list):
            parsed_skills = []

    except json.JSONDecodeError:
        parsed_skills = []

    resume_text = None

    if source == "resume":

        if resume is None:
            raise HTTPException(
                status_code=400,
                detail="A resume file is required when source is 'resume'.",
            )

        try:
            resume_bytes = await resume.read()
            filename = resume.filename or "resume.pdf"
            
            # Use unified shared extraction
            from app.services.rag.document_loader import extract_from_bytes
            resume_text = extract_from_bytes(resume_bytes, filename)

        except ValueError as exc:
            raise HTTPException(
                status_code=400,
                detail=str(exc),
            ) from exc

        if not resume_text:
            raise HTTPException(
                status_code=400,
                detail="Could not extract any text from the resume PDF.",
            )

    session, first_question = start_interview(
        db,
        source=source,
        role=role,
        skills=parsed_skills,
        resume_text=resume_text,
        mode=mode,
        duration_minutes=duration,
        question_count=question_count,
        api_provider=api_provider,
        api_key=groq_api_key,
        security_mode=security_mode,
    )

    return StartInterviewResponse(
        session_id=session.id,
        question_number=1,
        total_questions=session.total_questions,
        question=first_question,
        is_complete=False,
    )


@router.post(
    "/{session_id}/answer",
    response_model=AnswerResponse,
)
async def answer(
    session_id: str,
    payload: AnswerRequest,
    db: Session = Depends(get_db),
):

    if not payload.answer.strip():
        raise HTTPException(
            status_code=400,
            detail="Answer cannot be empty.",
        )

    try:

        result = submit_answer(
            db,
            session_id,
            payload.answer,
        )

    except InterviewNotFoundError as exc:

        raise HTTPException(
            status_code=404,
            detail="Interview session not found or expired.",
        ) from exc

    except InterviewCompleteError as exc:

        raise HTTPException(
            status_code=409,
            detail="This interview has already been completed.",
        ) from exc

    return result


@router.post(
    "/{session_id}/voice-answer",
    response_model=VoiceAnswerResponse,
)
async def voice_answer(
    session_id: str,
    audio: UploadFile = File(...),
    db: Session = Depends(get_db),
):

    session = get_session(db, session_id)

    if session is None:
        raise HTTPException(
            status_code=404,
            detail="Interview session not found or expired.",
        )

    audio_bytes = await audio.read()

    if not audio_bytes:
        raise HTTPException(
            status_code=400,
            detail="Empty recording received.",
        )

    auth = get_session_auth(session_id)
    text = transcribe_audio(
        audio_bytes,
        filename=audio.filename or "answer.webm",
        api_provider=auth["api_provider"],
        api_key=auth["api_key"],
    )

    return VoiceAnswerResponse(
        text=text
    )


@router.post(
    "/{session_id}/replay-question",
    response_model=ReplayQuestionResponse,
)
async def replay_question(
    session_id: str,
    db: Session = Depends(get_db),
):

    session = get_session(db, session_id)

    if session is None:
        raise HTTPException(
            status_code=404,
            detail="Interview session not found or expired.",
        )

    current_turn = session.current_turn

    if current_turn is None:
        raise HTTPException(
            status_code=409,
            detail="No active question for this session.",
        )

    return ReplayQuestionResponse(
        question=current_turn.question
    )


@router.post(
    "/{session_id}/speak"
)
async def speak(
    session_id: str,
    payload: SpeakRequest,
    db: Session = Depends(get_db),
):

    session = get_session(db, session_id)

    if session is None:
        raise HTTPException(
            status_code=404,
            detail="Interview session not found or expired.",
        )

    auth = get_session_auth(session_id)
    audio_bytes = synthesize_speech(
        payload.text,
        api_provider=auth["api_provider"],
        api_key=auth["api_key"],
    )

    return Response(
        content=audio_bytes,
        media_type="audio/wav",
    )


from app.schemas import PaginatedResponse, MockInterviewHistoryItem, FinalEvaluation, CompleteInterviewRequest
from fastapi import Body

@router.post(
    "/{session_id}/complete"
)
async def complete(
    session_id: str,
    payload: CompleteInterviewRequest | None = None,
    db: Session = Depends(get_db),
):

    session = get_session(db, session_id)

    if session is None:
        raise HTTPException(
            status_code=404,
            detail="Interview session not found or expired.",
        )

    if payload and payload.proctoring_metadata:
        if session.security_mode != "proctored":
            raise HTTPException(
                status_code=400,
                detail="Cannot submit proctoring metadata for a standard interview.",
            )
        session.proctoring_metadata = payload.proctoring_metadata

    session.is_complete = True

    final = build_final_evaluation(
        session
    )
    
    # final is already a dictionary returned by build_final_evaluation
    session.final_evaluation = final
    save_session(db, session)

    return final

from app.models.interview import InterviewSessionModel

@router.get("/history", response_model=PaginatedResponse[MockInterviewHistoryItem])
async def get_history(page: int = 1, page_size: int = 10, db: Session = Depends(get_db)):
    offset = (page - 1) * page_size
    total = db.query(InterviewSessionModel).count()
    items = db.query(InterviewSessionModel).order_by(InterviewSessionModel.created_at.desc()).offset(offset).limit(page_size).all()
    
    response_items = []
    for item in items:
        overall = item.final_evaluation.get("overall_score") if isinstance(item.final_evaluation, dict) else None
        
        if overall is None and item.turns:
            valid_turns = [t for t in item.turns if t.evaluation and isinstance(t.evaluation, dict) and "score" in t.evaluation]
            if valid_turns:
                overall = sum(t.evaluation.get("score", 0) for t in valid_turns) // len(valid_turns)
                
        response_items.append({
            "id": str(item.id),
            "created_at": item.created_at,
            "role": item.role or "Unknown",
            "mode": item.mode or "standard",
            "total_questions": int(item.total_questions) if item.total_questions is not None else 0,
            "overall_score": overall,
            "is_complete": bool(item.is_complete),
            "security_mode": str(item.security_mode),
            "proctoring_metadata": item.proctoring_metadata if isinstance(item.proctoring_metadata, list) else None
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
    history_item = db.query(InterviewSessionModel).filter(InterviewSessionModel.id == id).first()
    if not history_item:
        raise HTTPException(404, "History not found")
        
    return {
        "id": history_item.id,
        "created_at": history_item.created_at,
        "role": history_item.role,
        "skills": history_item.skills,
        "mode": history_item.mode,
        "duration_minutes": history_item.duration_minutes,
        "total_questions": history_item.total_questions,
        "is_complete": history_item.is_complete,
        "security_mode": history_item.security_mode,
        "proctoring_metadata": history_item.proctoring_metadata,
        "final_evaluation": history_item.final_evaluation,
        "turns": [
            {
                "turn_index": t.turn_index,
                "question": t.question,
                "answer": t.answer,
                "evaluation": t.evaluation
            }
            for t in history_item.turns
        ]
    }
