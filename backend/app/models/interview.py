import uuid
from datetime import datetime

from sqlalchemy import Column, String, Boolean, JSON, DateTime, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base


class InterviewSessionModel(Base):
    __tablename__ = "interview_sessions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    role = Column(String, nullable=False)
    skills = Column(JSON, nullable=False)
    resume_text = Column(String, nullable=True)
    mode = Column(String, nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    total_questions = Column(Integer, nullable=False)
    question_bank = Column(JSON, nullable=True, default=list)
    current_question_number = Column(Integer, default=0)
    api_key = Column(String, nullable=True)
    is_complete = Column(Boolean, default=False)
    final_evaluation = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    turns = relationship(
        "InterviewTurnModel", 
        back_populates="session",
        cascade="all, delete-orphan",
        order_by="InterviewTurnModel.turn_index"
    )

    @property
    def current_turn(self):
        return self.turns[-1] if self.turns else None

    def history_for_prompt(self) -> list[dict[str, str]]:
        return [
            {"question": t.question, "answer": t.answer or ""}
            for t in self.turns
            if t.answer
        ]

    def evaluations(self) -> list[dict]:
        return [t.evaluation for t in self.turns if t.evaluation]


class InterviewTurnModel(Base):
    __tablename__ = "interview_turns"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String, ForeignKey("interview_sessions.id"), nullable=False)
    turn_index = Column(Integer, nullable=False)
    question = Column(String, nullable=False)
    answer = Column(String, nullable=True)
    evaluation = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    session = relationship("InterviewSessionModel", back_populates="turns")
