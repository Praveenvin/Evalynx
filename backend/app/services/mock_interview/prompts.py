"""
All interview-related prompts live here, kept separate from the services
that call them so they're easy to review and tune independently.
"""

INTERVIEWER_SYSTEM_PROMPT = """You are an AI technical interviewer for Evalynx.

Conduct a professional, realistic interview. Use only the candidate
information provided to you (target role, selected skills, and/or resume
text) - never invent candidate experience that wasn't given to you.

Ask one question at a time. Questions should be relevant to the target
role, selected skills, and any resume evidence provided.

For dynamic interviews, use the candidate's previous answer to decide what
to ask next - do not ask an unrelated question just because it's next in a
list.

Mix question types across the interview: technical questions, practical
questions, project questions, problem-solving questions, and behavioral
questions. Avoid repeating similar questions.

Never reveal evaluation scores or feedback during the interview itself.

Keep each question concise enough to be spoken naturally out loud (roughly
one to three sentences)."""


def build_first_question_prompt(
    *, role: str, skills: list[str], resume_text: str | None, mode: str
) -> list[dict[str, str]]:
    context_lines = [f"Target role: {role}"] if role else []
    if skills:
        context_lines.append(f"Candidate skills: {', '.join(skills)}")
    if resume_text:
        context_lines.append(
            f"Resume excerpt (use only what is actually stated here):\n{resume_text[:4000]}"
        )
    context_lines.append(f"Interview mode: {mode}")

    user_prompt = (
        "\n".join(context_lines)
        + "\n\nGenerate the first interview question only. "
        "Return plain text, no numbering, no preamble - just the question."
    )
    return [
        {"role": "system", "content": INTERVIEWER_SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ]


def build_question_bank_prompt(
    *, role: str, skills: list[str], resume_text: str | None, question_count: int
) -> list[dict[str, str]]:
    """Used for STANDARD mode - generate the full question set upfront."""
    context_lines = [f"Target role: {role}"] if role else []
    if skills:
        context_lines.append(f"Candidate skills: {', '.join(skills)}")
    if resume_text:
        context_lines.append(
            f"Resume excerpt (use only what is actually stated here):\n{resume_text[:4000]}"
        )

    user_prompt = (
        "\n".join(context_lines)
        + f"\n\nGenerate exactly {question_count} interview questions for this "
        "candidate, ordered from warm-up to more in-depth. Mix technical, "
        "practical, project, problem-solving, and behavioral questions. "
        'Respond as JSON: {"questions": ["question 1", "question 2", ...]}'
    )
    return [
        {"role": "system", "content": INTERVIEWER_SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ]


def build_next_question_prompt(
    *,
    role: str,
    skills: list[str],
    resume_text: str | None,
    history: list[dict[str, str]],
    previous_question: str,
    previous_answer: str,
) -> list[dict[str, str]]:
    """Used for DYNAMIC mode - decide the next question from context."""
    context_lines = [f"Target role: {role}"] if role else []
    if skills:
        context_lines.append(f"Candidate skills: {', '.join(skills)}")
    if resume_text:
        context_lines.append(
            f"Resume excerpt (use only what is actually stated here):\n{resume_text[:4000]}"
        )

    transcript = "\n".join(
        f"Q: {turn['question']}\nA: {turn['answer']}" for turn in history
    )

    user_prompt = (
        "\n".join(context_lines)
        + (f"\n\nInterview so far:\n{transcript}" if transcript else "")
        + f"\n\nMost recent question: {previous_question}"
        + f"\nMost recent answer: {previous_answer}"
        + "\n\nBased on this answer, generate the single best next question. "
        "It should follow naturally from what the candidate just said, "
        "probe deeper or pivot to a new relevant area as appropriate, and "
        "must not repeat a previous question. Return plain text only - the "
        "question itself, nothing else."
    )
    return [
        {"role": "system", "content": INTERVIEWER_SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ]


EVALUATION_SYSTEM_PROMPT = """You are an AI interview evaluator.

For each candidate answer, evaluate technical knowledge, correctness,
relevance to the question, problem solving, communication, and clarity.

Be conservative. Do not give credit for claims that go beyond what the
candidate actually said. If the question is resume-based, do not give
credit for skills or experience not supported by the resume.

Respond ONLY with JSON in this exact shape:
{
  "score": 0,
  "technical_score": 0,
  "communication_score": 0,
  "problem_solving_score": 0,
  "relevance_score": 0,
  "feedback": "",
  "strengths": [],
  "improvements": []
}
All scores are integers from 0 to 100."""


def build_answer_evaluation_prompt(
    *, role: str, skills: list[str], question: str, answer: str
) -> list[dict[str, str]]:
    user_prompt = (
        f"Target role: {role}\n"
        f"Candidate skills: {', '.join(skills) if skills else 'n/a'}\n\n"
        f"Question: {question}\n"
        f"Candidate answer: {answer}\n\n"
        "Evaluate this answer now."
    )
    return [
        {"role": "system", "content": EVALUATION_SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ]


FINAL_SUMMARY_SYSTEM_PROMPT = """You are an AI interview evaluator writing a
final summary. You will be given the per-answer evaluations from an entire
interview. Do not invent new scores - just summarize the pattern of
strengths and areas to improve across the whole interview, and write a
short (2-4 sentence) overall summary in a professional, encouraging tone."""


def build_final_summary_prompt(
    *, role: str, per_answer_evaluations: list[dict]
) -> list[dict[str, str]]:
    evaluations_text = "\n\n".join(
        f"Q{i + 1} feedback: {ev.get('feedback', '')}\n"
        f"Strengths: {', '.join(ev.get('strengths', []))}\n"
        f"Improvements: {', '.join(ev.get('improvements', []))}"
        for i, ev in enumerate(per_answer_evaluations)
    )
    user_prompt = (
        f"Target role: {role}\n\nPer-question evaluations:\n{evaluations_text}\n\n"
        "Respond ONLY with JSON in this exact shape:\n"
        '{"strengths": [], "areas_to_improve": [], "summary": ""}\n'
        "strengths and areas_to_improve should each be 2-4 short bullet points "
        "aggregated across the whole interview, not per-question."
    )
    return [
        {"role": "system", "content": FINAL_SUMMARY_SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ]