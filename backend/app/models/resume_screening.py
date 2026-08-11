import uuid
from datetime import datetime

from sqlalchemy import (
    Column,
    String,
    Float,
    Integer,
    JSON,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import relationship

from app.core.database import Base


class ResumeScreeningModel(Base):
    __tablename__ = "resume_screenings"

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    job_description = Column(String, nullable=False)
    status = Column(String, nullable=False, default="processing")
    created_at = Column(DateTime, default=datetime.utcnow)

    candidates = relationship(
        "ResumeCandidateModel",
        back_populates="screening",
        cascade="all, delete-orphan",
        order_by="ResumeCandidateModel.overall_score.desc()",
    )


class ResumeCandidateModel(Base):
    __tablename__ = "resume_candidates"

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    screening_id = Column(
        String,
        ForeignKey("resume_screenings.id"),
        nullable=False,
    )
    filename = Column(String, nullable=False)
    candidate_name = Column(String, nullable=True)
    email = Column(String, nullable=True)
    
    overall_score = Column(Float, nullable=False, default=0.0)
    skills_score = Column(Float, nullable=False, default=0.0)
    experience_score = Column(Float, nullable=False, default=0.0)
    education_score = Column(Float, nullable=False, default=0.0)
    semantic_score = Column(Float, nullable=False, default=0.0)
    
    strengths = Column(JSON, nullable=True, default=list)
    gaps = Column(JSON, nullable=True, default=list)
    recommendation = Column(String, nullable=True)
    rank = Column(Integer, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)

    screening = relationship(
        "ResumeScreeningModel",
        back_populates="candidates",
    )

    evidence = relationship(
        "ResumeEvidenceModel",
        back_populates="candidate",
        cascade="all, delete-orphan",
    )


class ResumeEvidenceModel(Base):
    __tablename__ = "resume_evidence"

    id = Column(Integer, primary_key=True, autoincrement=True)
    candidate_id = Column(
        String,
        ForeignKey("resume_candidates.id"),
        nullable=False,
    )
    text = Column(String, nullable=False)
    similarity_score = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    candidate = relationship(
        "ResumeCandidateModel",
        back_populates="evidence",
    )
