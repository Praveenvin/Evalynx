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