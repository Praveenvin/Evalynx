from typing import Literal

from pydantic import BaseModel, Field


InterviewSource = Literal["resume", "role"]
InterviewMode = Literal["standard", "dynamic"]


class StartInterviewRequest(BaseModel):
    source: InterviewSource
    role: str = ""
    skills: list[str] = Field(default_factory=list)
    mode: InterviewMode
    duration: int = Field(default=15, ge=1, le=60)
    question_count: int = Field(default=5, ge=1, le=20)
    api_provider: Literal["user", "evalynx"] = "evalynx"
    groq_api_key: str | None = None


class StartInterviewResponse(BaseModel):
    session_id: str
    question_number: int
    total_questions: int
    question: str
    is_complete: bool = False


class AnswerRequest(BaseModel):
    answer: str = Field(..., min_length=1)


class AnswerEvaluation(BaseModel):
    score: int
    technical_score: int
    communication_score: int
    problem_solving_score: int
    relevance_score: int
    feedback: str
    strengths: list[str] = Field(default_factory=list)
    improvements: list[str] = Field(default_factory=list)


class FinalEvaluation(BaseModel):
    overall_score: int
    technical_knowledge: int
    communication: int
    problem_solving: int
    confidence_clarity: int
    strengths: list[str]
    areas_to_improve: list[str]
    summary: str


class AnswerResponse(BaseModel):
    evaluation: AnswerEvaluation
    next_question: str | None
    question_number: int
    is_complete: bool
    final_evaluation: FinalEvaluation | None = None


class VoiceAnswerResponse(BaseModel):
    text: str


class SpeakRequest(BaseModel):
    text: str


class ReplayQuestionResponse(BaseModel):
    question: str


# --- Course Recommendation Schemas ---

from pydantic import field_validator

class StudentProfile(BaseModel):
    name: str = Field(..., min_length=1)
    education: str = ""
    background: str = ""
    career_goal: str = Field(..., min_length=1)
    current_skills: list[str] = Field(default_factory=list)
    interests: list[str] = Field(default_factory=list)
    api_provider: Literal["user", "evalynx"] = "evalynx"
    groq_api_key: str | None = None

    @field_validator("current_skills", "interests", mode="before")
    @classmethod
    def _drop_blanks(cls, value):
        if not value:
            return []
        return [v.strip() for v in value if isinstance(v, str) and v.strip()]


class LearningPathStep(BaseModel):
    step: int
    course: str
    reason: str
    difficulty: str
    prerequisites: list[str]
    duration: str
    skills_gained: list[str]


class CourseRecommendationResponse(BaseModel):
    student: StudentProfile
    career_goal: str
    current_skills: list[str]
    skill_gaps: list[str] = Field(default_factory=list)
    learning_path: list[LearningPathStep]
    summary: str
    goal_supported: bool = True

from datetime import datetime
from typing import Generic, TypeVar, Any

T = TypeVar("T")

class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T]
    page: int
    page_size: int
    total: int
    total_pages: int

class ResumeScreeningHistoryItem(BaseModel):
    id: str
    created_at: datetime
    job_description: str
    candidate_count: int
    top_score: float | None
    status: str

class MockInterviewHistoryItem(BaseModel):
    id: str
    created_at: datetime
    role: str
    mode: str
    total_questions: int
    overall_score: int | None
    is_complete: bool

class CourseRecommendationHistoryItem(BaseModel):
    id: str
    created_at: datetime
    student_name: str
    career_goal: str
    course_count: int