"""
PostgreSQL-backed interview session state using SQLAlchemy.
"""
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.models.interview import InterviewSessionModel, InterviewTurnModel

# Re-export models for compatibility with other modules expecting these names
InterviewSession = InterviewSessionModel
InterviewTurn = InterviewTurnModel

def create_session(db: Session, **kwargs) -> InterviewSession:
    # Handle the 'source' argument which is not in our model
    kwargs.pop("source", None)
    
    session = InterviewSessionModel(**kwargs)
    db.add(session)
    db.commit()
    db.refresh(session)
    return session

def get_session(db: Session, session_id: str) -> InterviewSession | None:
    return db.query(InterviewSessionModel).filter(InterviewSessionModel.id == session_id).first()

def delete_session(db: Session, session_id: str) -> None:
    session = get_session(db, session_id)
    if session:
        db.delete(session)
        db.commit()

def save_session(db: Session, session: InterviewSession) -> None:
    """Helper method to explicitly commit changes to a session."""
    db.commit()
    db.refresh(session)