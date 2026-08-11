from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas import CourseRecommendationResponse, StudentProfile
from app.services.course_recommendation.recommendation_service import generate_recommendation
from app.models.course_recommendation import CourseRecommendationHistoryModel, RecommendedCoursePathModel

router = APIRouter(prefix="/api/course-recommendation", tags=["course-recommendation"])


@router.post("/recommend", response_model=CourseRecommendationResponse)
async def recommend(student: StudentProfile, db: Session = Depends(get_db)):
    if not student.career_goal.strip():
        raise HTTPException(400, "career_goal is required.")

    try:
        result = generate_recommendation(
            name=student.name,
            education=student.education,
            background=student.background,
            career_goal=student.career_goal,
            current_skills=student.current_skills,
            interests=student.interests,
            api_key=student.groq_api_key,
        )
    except Exception as exc:  # defensive: never let this endpoint 500 silently
        raise HTTPException(502, f"Could not generate a recommendation: {exc}") from exc

    # Persist to database
    db_history = CourseRecommendationHistoryModel(
        student_name=student.name,
        education=student.education,
        background=student.background,
        career_goal=student.career_goal,
        current_skills=student.current_skills,
        interests=student.interests,
        summary=result["summary"]
    )
    db.add(db_history)
    db.flush() # To get db_history.id

    for step_data in result["learning_path"]:
        db_path = RecommendedCoursePathModel(
            recommendation_id=db_history.id,
            step=step_data["step"],
            course=step_data["course"],
            reason=step_data["reason"],
            difficulty=step_data["difficulty"],
            prerequisites=step_data["prerequisites"],
            duration=step_data["duration"],
            skills_gained=step_data["skills_gained"]
        )
        db.add(db_path)
    
    db.commit()

    # Clear API key before returning so it never appears in response JSON
    student.groq_api_key = None

    return CourseRecommendationResponse(student=student, **result)
