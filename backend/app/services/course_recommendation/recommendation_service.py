"""
Core logic for the Course Recommendation agent.

The learning path, skill gaps, and course choices are fully driven by the LLM
evaluating the student's profile against the available catalogue.
"""
import logging

from app.services.llm.groq_client import GroqServiceError, chat_completion_json
from app.services.course_recommendation.catalogue import Course, get_all_courses, get_course
from app.services.course_recommendation.prompts import build_recommendation_prompt

logger = logging.getLogger(__name__)


def generate_recommendation(
    *,
    name: str,
    education: str,
    background: str,
    career_goal: str,
    current_skills: list[str],
    interests: list[str],
    api_provider: str = "evalynx",
    api_key: str | None = None,
) -> dict:
    
    catalogue = get_all_courses()
    catalogue_dicts = [
        {
            "id": c.id,
            "name": c.name,
            "category": c.category,
            "career_roles": getattr(c, "career_roles", []),
            "keywords": getattr(c, "keywords", []),
            "related_skills": getattr(c, "related_skills", []),
            "difficulty": c.difficulty,
            "prerequisites": [p.name for p_id in c.prerequisites if (p := get_course(p_id))],
            "duration": c.duration,
            "skills_gained": c.skills_gained,
        }
        for c in catalogue
    ]

    messages = build_recommendation_prompt(
        name=name,
        background=background,
        education=education,
        career_goal=career_goal,
        current_skills=current_skills,
        interests=interests,
        catalogue=catalogue_dicts,
    )

    prompt_chars = sum(len(m["content"]) for m in messages)
    logger.info(f"Course Recommendation LLM Request: {len(catalogue)} courses, ~{prompt_chars} chars.")

    try:
        result = chat_completion_json(
            messages,
            temperature=0.3,
            max_tokens=2000,
            api_provider=api_provider,
            api_key=api_key,
        )
    except GroqServiceError:
        raise
    
    goal_supported = result.get("goal_supported", True)
    skill_gaps = result.get("skill_gaps", [])
    learning_path_raw = result.get("learning_path", [])
    summary = result.get("summary", "")

    learning_path = []
    if goal_supported:
        for i, step in enumerate(learning_path_raw, start=1):
            learning_path.append(
                {
                    "step": i,
                    "course": step.get("course", "Unknown Course"),
                    "reason": step.get("reason", "Highly recommended."),
                    "difficulty": step.get("difficulty", "Beginner"),
                    "prerequisites": step.get("prerequisites", []),
                    "duration": step.get("duration", "Unknown"),
                    "skills_gained": step.get("skills_gained", []),
                }
            )

    return {
        "career_goal": career_goal,
        "current_skills": sorted(current_skills, key=str.lower),
        "skill_gaps": skill_gaps,
        "learning_path": learning_path,
        "summary": summary,
        "goal_supported": goal_supported,
    }


def list_catalogue() -> list[Course]:
    return get_all_courses()
