import json
import logging

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import Response

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
):
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

            resume_text = extract_resume_text(
                resume_bytes
            )

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

    try:

        session, first_question = start_interview(
            source=source,
            role=role,
            skills=parsed_skills,
            resume_text=resume_text,
            mode=mode,
            duration_minutes=duration,
            question_count=question_count,
        )

    except GroqServiceError as exc:

        raise HTTPException(
            status_code=502,
            detail=f"AI service is unavailable: {exc}",
        ) from exc

    return StartInterviewResponse(
        session_id=session.session_id,
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
):

    if not payload.answer.strip():
        raise HTTPException(
            status_code=400,
            detail="Answer cannot be empty.",
        )

    try:

        result = submit_answer(
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

    except GroqServiceError as exc:

        raise HTTPException(
            status_code=502,
            detail=f"AI service is unavailable: {exc}",
        ) from exc

    return result


@router.post(
    "/{session_id}/voice-answer",
    response_model=VoiceAnswerResponse,
)
async def voice_answer(
    session_id: str,
    audio: UploadFile = File(...),
):

    session = get_session(session_id)

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

    try:

        text = transcribe_audio(
            audio_bytes,
            filename=audio.filename or "answer.webm",
        )

    except GroqServiceError as exc:

        raise HTTPException(
            status_code=502,
            detail=f"Transcription failed: {exc}",
        ) from exc

    return VoiceAnswerResponse(
        text=text
    )


@router.post(
    "/{session_id}/replay-question",
    response_model=ReplayQuestionResponse,
)
async def replay_question(
    session_id: str,
):

    session = get_session(session_id)

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
):

    session = get_session(session_id)

    if session is None:
        raise HTTPException(
            status_code=404,
            detail="Interview session not found or expired.",
        )

    try:

        audio_bytes = synthesize_speech(
            payload.text
        )

    except GroqServiceError as exc:

        raise HTTPException(
            status_code=502,
            detail=f"Speech synthesis failed: {exc}",
        ) from exc

    return Response(
        content=audio_bytes,
        media_type="audio/wav",
    )


@router.post(
    "/{session_id}/complete"
)
async def complete(
    session_id: str,
):

    session = get_session(session_id)

    if session is None:
        raise HTTPException(
            status_code=404,
            detail="Interview session not found or expired.",
        )

    session.is_complete = True

    try:

        final = build_final_evaluation(
            session
        )

    except GroqServiceError as exc:

        raise HTTPException(
            status_code=502,
            detail=f"AI service is unavailable: {exc}",
        ) from exc

    return final
