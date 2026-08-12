from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas import CourseRecommendationResponse, StudentProfile
from app.services.course_recommendation.recommendation_service import generate_recommendation
from app.services.llm.groq_client import GroqServiceError
from app.models.course_recommendation import CourseRecommendationHistoryModel, RecommendedCoursePathModel

router = APIRouter(prefix="/api/course-recommendation", tags=["course-recommendation"])


@router.post("/recommend", response_model=CourseRecommendationResponse)
async def recommend(student: StudentProfile, db: Session = Depends(get_db)):
    if not student.career_goal.strip():
        raise HTTPException(400, "career_goal is required.")

    if student.api_provider == "user" and (not student.groq_api_key or not student.groq_api_key.strip()):
        raise GroqServiceError("Please enter your Groq API key.", code="MISSING_API_KEY")

    try:
        result = generate_recommendation(
            name=student.name,
            education=student.education,
            background=student.background,
            career_goal=student.career_goal,
            current_skills=student.current_skills,
            interests=student.interests,
            api_provider=student.api_provider,
            api_key=student.groq_api_key,
        )
    except GroqServiceError:
        raise
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

from app.schemas import PaginatedResponse, CourseRecommendationHistoryItem

@router.get("/history", response_model=PaginatedResponse[CourseRecommendationHistoryItem])
async def get_history(page: int = 1, page_size: int = 10, db: Session = Depends(get_db)):
    offset = (page - 1) * page_size
    total = db.query(CourseRecommendationHistoryModel).count()
    items = db.query(CourseRecommendationHistoryModel).order_by(CourseRecommendationHistoryModel.created_at.desc()).offset(offset).limit(page_size).all()
    
    return {
        "items": [
            {
                "id": item.id,
                "created_at": item.created_at,
                "student_name": item.student_name,
                "career_goal": item.career_goal,
                "course_count": len(item.paths)
            }
            for item in items
        ],
        "page": page,
        "page_size": page_size,
        "total": total,
        "total_pages": (total + page_size - 1) // page_size
    }

@router.get("/history/{id}", response_model=CourseRecommendationResponse)
async def get_history_detail(id: str, db: Session = Depends(get_db)):
    history_item = db.query(CourseRecommendationHistoryModel).filter(CourseRecommendationHistoryModel.id == id).first()
    if not history_item:
        raise HTTPException(404, "History not found")
        
    student_profile = StudentProfile(
        name=history_item.student_name,
        education=history_item.education or "",
        background=history_item.background or "",
        career_goal=history_item.career_goal,
        current_skills=history_item.current_skills,
        interests=history_item.interests,
        api_provider="evalynx" # Default metadata
    )
    
    learning_path = [
        {
            "step": path.step,
            "course": path.course,
            "reason": path.reason,
            "difficulty": path.difficulty,
            "prerequisites": path.prerequisites,
            "duration": path.duration,
            "skills_gained": path.skills_gained
        }
        for path in history_item.paths
    ]
    
    return CourseRecommendationResponse(
        student=student_profile,
        career_goal=history_item.career_goal,
        current_skills=history_item.current_skills,
        skill_gaps=[],
        learning_path=learning_path,
        summary=history_item.summary,
        goal_supported=True
    )

