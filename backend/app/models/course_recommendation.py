import uuid
from datetime import datetime

from sqlalchemy import Column, String, JSON, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.core.database import Base


class CourseRecommendationHistoryModel(Base):
    __tablename__ = "course_recommendations"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    student_name = Column(String, nullable=False)
    education = Column(String, nullable=True)
    background = Column(String, nullable=True)
    career_goal = Column(String, nullable=False)
    current_skills = Column(JSON, nullable=False, default=list)
    interests = Column(JSON, nullable=False, default=list)
    summary = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    paths = relationship(
        "RecommendedCoursePathModel",
        back_populates="recommendation",
        cascade="all, delete-orphan",
        order_by="RecommendedCoursePathModel.step"
    )

class RecommendedCoursePathModel(Base):
    __tablename__ = "recommended_course_paths"

    id = Column(Integer, primary_key=True, autoincrement=True)
    recommendation_id = Column(String, ForeignKey("course_recommendations.id"), nullable=False)
    step = Column(Integer, nullable=False)
    course = Column(String, nullable=False)
    reason = Column(String, nullable=False)
    difficulty = Column(String, nullable=False)
    prerequisites = Column(JSON, nullable=False, default=list)
    duration = Column(String, nullable=False)
    skills_gained = Column(JSON, nullable=False, default=list)

    recommendation = relationship("CourseRecommendationHistoryModel", back_populates="paths")
