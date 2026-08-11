"""
Core logic for the Course Recommendation agent.

Skill-gap analysis and learning-path ordering are fully deterministic
(structured catalogue + career path data). The Groq LLM is only used to
phrase the per-course "reason" and the overall "summary" - see
prompts.py. If Groq is unavailable, a template-based fallback is used so
the endpoint never fails just because the AI call failed.
"""
import logging

from app.services.llm.groq_client import GroqServiceError, chat_completion_json
from app.services.course_recommendation.catalogue import Course, get_all_courses, get_course
from app.services.course_recommendation.career_paths import CAREER_PATHS, match_career_path
from app.services.course_recommendation.prompts import build_recommendation_prompt

logger = logging.getLogger(__name__)


def _normalize(values: list[str]) -> set[str]:
    return {v.strip().lower() for v in values if v and v.strip()}


def _course_already_known(course: Course, known_skills: set[str]) -> bool:
    if course.name.lower() in known_skills:
        return True
    return any(skill.lower() in known_skills for skill in course.skills_gained)


def _prereq_names(course: Course) -> list[str]:
    return [p.name for pid in course.prerequisites if (p := get_course(pid)) is not None]


def _fallback_reason(course: Course, career_goal: str) -> str:
    prereq_names = _prereq_names(course)
    if prereq_names:
        return f"Builds directly on {', '.join(prereq_names)} toward your goal of {career_goal}."
    return f"Provides a strong foundation relevant to becoming a {career_goal}."


def generate_recommendation(
    *,
    name: str,
    education: str,
    background: str,
    career_goal: str,
    current_skills: list[str],
    interests: list[str],
    api_key: str | None = None,
) -> dict:
    known_skills = _normalize(current_skills)

    path_key = match_career_path(career_goal)
    target_ids = CAREER_PATHS[path_key]

    gap_courses: list[Course] = []
    for course_id in target_ids:
        course = get_course(course_id)
        if course is None:
            continue
        if not _course_already_known(course, known_skills):
            gap_courses.append(course)

    if not gap_courses:
        return {
            "career_goal": career_goal,
            "current_skills": sorted(current_skills, key=str.lower),
            "skill_gaps": [],
            "learning_path": [],
            "summary": (
                f"Based on your current skills, you already cover the core skills "
                f"typically needed for {career_goal or 'this goal'}. Consider exploring "
                f"more advanced or specialized topics next."
            ),
        }

    path_courses_for_prompt = [
        {
            "name": c.name,
            "prerequisites": _prereq_names(c),
            "skills_gained": c.skills_gained,
        }
        for c in gap_courses
    ]

    reasons: dict[str, str] = {}
    summary = ""
    try:
        result = chat_completion_json(
            build_recommendation_prompt(
                name=name,
                background=background,
                education=education,
                career_goal=career_goal,
                current_skills=current_skills,
                interests=interests,
                path_courses=path_courses_for_prompt,
            ),
            temperature=0.5,
            max_tokens=800,
            api_key=api_key,
        )
        reasons = result.get("reasons", {}) or {}
        summary = result.get("summary", "") or ""
    except GroqServiceError:
        logger.warning("Course recommendation reasoning failed, using fallback text")

    learning_path = []
    for i, course in enumerate(gap_courses, start=1):
        reason = reasons.get(course.name) or _fallback_reason(course, career_goal)
        learning_path.append(
            {
                "step": i,
                "course": course.name,
                "reason": reason,
                "difficulty": course.difficulty,
                "prerequisites": _prereq_names(course),
                "duration": course.duration,
                "skills_gained": course.skills_gained,
            }
        )

    if not summary:
        names = ", ".join(step["course"] for step in learning_path)
        summary = (
            f"This {len(learning_path)}-step path takes you from your current skills "
            f"toward {career_goal or 'your goal'}, covering {names}."
        )

    return {
        "career_goal": career_goal,
        "current_skills": sorted(current_skills, key=str.lower),
        "skill_gaps": [c.name for c in gap_courses],
        "learning_path": learning_path,
        "summary": summary,
    }


def list_catalogue() -> list[Course]:
    return get_all_courses()
