"""
Temporary in-memory interview session state.

Not persisted - fine for a single-process dev/demo backend. Swap this for
PostgreSQL-backed storage later without changing the router/service layer,
since everything goes through this module's functions.
"""
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone


@dataclass
class InterviewTurn:
    question: str
    answer: str | None = None
    evaluation: dict | None = None


@dataclass
class InterviewSession:
    session_id: str
    source: str  # "resume" | "role"
    role: str
    skills: list[str]
    resume_text: str | None
    mode: str  # "standard" | "dynamic"
    duration_minutes: int
    total_questions: int
    question_bank: list[str] = field(default_factory=list)  # standard mode only
    turns: list[InterviewTurn] = field(default_factory=list)
    current_question_number: int = 0
    is_complete: bool = False
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def current_turn(self) -> InterviewTurn | None:
        return self.turns[-1] if self.turns else None

    def history_for_prompt(self) -> list[dict[str, str]]:
        return [
            {"question": t.question, "answer": t.answer or ""}
            for t in self.turns
            if t.answer
        ]

    def evaluations(self) -> list[dict]:
        return [t.evaluation for t in self.turns if t.evaluation]


_SESSIONS: dict[str, InterviewSession] = {}
_SESSION_TTL = timedelta(hours=3)


def create_session(**kwargs) -> InterviewSession:
    session_id = str(uuid.uuid4())
    session = InterviewSession(session_id=session_id, **kwargs)
    _SESSIONS[session_id] = session
    return session


def get_session(session_id: str) -> InterviewSession | None:
    _evict_expired()
    return _SESSIONS.get(session_id)


def delete_session(session_id: str) -> None:
    _SESSIONS.pop(session_id, None)


def _evict_expired() -> None:
    now = datetime.now(timezone.utc)
    expired = [
        sid
        for sid, s in _SESSIONS.items()
        if now - s.created_at > _SESSION_TTL
    ]
    for sid in expired:
        _SESSIONS.pop(sid, None)