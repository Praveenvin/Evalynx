from pydantic import BaseModel, Field, field_validator


class StudentProfile(BaseModel):
    name: str = Field(..., min_length=1)
    education: str = ""
    background: str = ""
    career_goal: str = Field(..., min_length=1)
    current_skills: list[str] = Field(default_factory=list)
    interests: list[str] = Field(default_factory=list)

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
    skill_gaps: list[str]
    learning_path: list[LearningPathStep]
    summary: str
