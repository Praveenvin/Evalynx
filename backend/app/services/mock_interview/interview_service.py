"""
Orchestrates the interview: creating sessions, generating questions
(standard vs dynamic), evaluating answers, and producing the final score.
Routers should call into this module rather than touching Groq or the
session store directly.
"""
import logging

from app.services.llm.groq_client import (
    GroqServiceError,
    chat_completion,
    chat_completion_json,
)

from app.services.mock_interview.prompts import (
    build_answer_evaluation_prompt,
    build_final_summary_prompt,
    build_first_question_prompt,
    build_next_question_prompt,
    build_question_bank_prompt,
)

from app.services.mock_interview.scoring import (
    calculate_final_scores,
)

from app.services.mock_interview.session_store import (
    InterviewSession,
    InterviewTurn,
    create_session,
    get_session,
)

logger = logging.getLogger(__name__)


class InterviewNotFoundError(Exception):
    pass


class InterviewCompleteError(Exception):
    pass
def start_interview(
    *,
    source: str,
    role: str,
    skills: list[str],
    resume_text: str | None,
    mode: str,
    duration_minutes: int,
    question_count: int,
) -> tuple[InterviewSession, str]:
    session = create_session(
        source=source,
        role=role,
        skills=skills,
        resume_text=resume_text,
        mode=mode,
        duration_minutes=duration_minutes,
        total_questions=question_count,
    )

    if mode == "standard":
        bank = _generate_question_bank(
            role=role, skills=skills, resume_text=resume_text, question_count=question_count
        )
        session.question_bank = bank
        first_question = bank[0] if bank else _fallback_question(role)
    else:
        first_question = _generate_first_question(
            role=role, skills=skills, resume_text=resume_text, mode=mode
        )

    session.current_question_number = 1
    session.turns.append(InterviewTurn(question=first_question))
    return session, first_question


def submit_answer(session_id: str, answer: str) -> dict:
    session = get_session(session_id)
    if session is None:
        raise InterviewNotFoundError(session_id)
    if session.is_complete:
        raise InterviewCompleteError(session_id)

    current_turn = session.current_turn
    current_turn.answer = answer

    evaluation = _evaluate_answer(
        role=session.role,
        skills=session.skills,
        question=current_turn.question,
        answer=answer,
    )
    current_turn.evaluation = evaluation

    if session.current_question_number >= session.total_questions:
        session.is_complete = True
        final = build_final_evaluation(session)
        return {
            "evaluation": evaluation,
            "next_question": None,
            "question_number": session.current_question_number,
            "is_complete": True,
            "final_evaluation": final,
        }

    next_question = _next_question(session)
    session.current_question_number += 1
    session.turns.append(InterviewTurn(question=next_question))

    return {
        "evaluation": evaluation,
        "next_question": next_question,
        "question_number": session.current_question_number,
        "is_complete": False,
        "final_evaluation": None,
    }


def build_final_evaluation(session: InterviewSession) -> dict:
    evaluations = session.evaluations()
    scores = calculate_final_scores(evaluations)

    try:
        summary_response = chat_completion_json(
            build_final_summary_prompt(role=session.role, per_answer_evaluations=evaluations),
            temperature=0.5,
            max_tokens=500,
        )
        strengths = summary_response.get("strengths", [])
        improvements = summary_response.get("areas_to_improve", [])
        summary = summary_response.get("summary", "")
    except GroqServiceError:
        logger.warning("Final summary generation failed, falling back to per-answer data")
        strengths = _dedupe(
            [s for e in evaluations for s in e.get("strengths", [])]
        )[:4]
        improvements = _dedupe(
            [s for e in evaluations for s in e.get("improvements", [])]
        )[:4]
        summary = (
            "The candidate completed the interview. See individual question "
            "feedback for details."
        )

    return {
        **scores,
        "strengths": strengths or ["Completed the interview with relevant answers."],
        "areas_to_improve": improvements or ["Continue practicing structured answers."],
        "summary": summary,
    }


def _generate_first_question(
    *, role: str, skills: list[str], resume_text: str | None, mode: str
) -> str:
    try:
        return chat_completion(
            build_first_question_prompt(
                role=role, skills=skills, resume_text=resume_text, mode=mode
            ),
            temperature=0.7,
            max_tokens=150,
        ).strip()
    except GroqServiceError:
        logger.warning("First question generation failed, using fallback question")
        return _fallback_question(role)


def _generate_question_bank(
    *, role: str, skills: list[str], resume_text: str | None, question_count: int
) -> list[str]:
    try:
        data = chat_completion_json(
            build_question_bank_prompt(
                role=role,
                skills=skills,
                resume_text=resume_text,
                question_count=question_count,
            ),
            temperature=0.7,
            max_tokens=1200,
        )
        questions = [q for q in data.get("questions", []) if isinstance(q, str) and q.strip()]
        if questions:
            return questions[:question_count]
    except GroqServiceError:
        logger.warning("Question bank generation failed, using fallback bank")

    return [_fallback_question(role) for _ in range(question_count)]


def _next_question(session: InterviewSession) -> str:
    if session.mode == "standard":
        idx = session.current_question_number  # next index (0-based == next Q)
        if idx < len(session.question_bank):
            return session.question_bank[idx]
        return _fallback_question(session.role)

    current_turn = session.current_turn
    try:
        return chat_completion(
            build_next_question_prompt(
                role=session.role,
                skills=session.skills,
                resume_text=session.resume_text,
                history=session.history_for_prompt(),
                previous_question=current_turn.question,
                previous_answer=current_turn.answer or "",
            ),
            temperature=0.7,
            max_tokens=150,
        ).strip()
    except GroqServiceError:
        logger.warning("Dynamic next-question generation failed, using fallback question")
        return _fallback_question(session.role)


def _evaluate_answer(*, role: str, skills: list[str], question: str, answer: str) -> dict:
    try:
        result = chat_completion_json(
            build_answer_evaluation_prompt(role=role, skills=skills, question=question, answer=answer),
            temperature=0.3,
            max_tokens=500,
        )
        return {
            "score": int(result.get("score", 0)),
            "technical_score": int(result.get("technical_score", 0)),
            "communication_score": int(result.get("communication_score", 0)),
            "problem_solving_score": int(result.get("problem_solving_score", 0)),
            "relevance_score": int(result.get("relevance_score", 0)),
            "feedback": result.get("feedback", ""),
            "strengths": result.get("strengths", []),
            "improvements": result.get("improvements", []),
        }
    except (GroqServiceError, ValueError, TypeError):
        logger.warning("Answer evaluation failed, returning neutral fallback score")
        return {
            "score": 50,
            "technical_score": 50,
            "communication_score": 50,
            "problem_solving_score": 50,
            "relevance_score": 50,
            "feedback": "We couldn't score this answer automatically.",
            "strengths": [],
            "improvements": [],
        }


def _fallback_question(role: str) -> str:
    role_label = role or "this role"
    return f"Tell me about a project where you applied skills relevant to {role_label}."


def _dedupe(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result = []
    for item in items:
        if item and item not in seen:
            seen.add(item)
            result.append(item)
    return result
