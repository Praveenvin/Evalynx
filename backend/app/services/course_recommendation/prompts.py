"""
Prompt for turning the deterministically-computed learning path into
human-facing reasons and a short summary. The path, ordering, and
prerequisites are already decided by career_paths.py + catalogue.py before
this is called - the LLM only explains, it never chooses the courses.
"""

SYSTEM_PROMPT = """You are an AI academic advisor for Evalynx's Course
Recommendation agent. You will be given a student's profile and a
pre-decided, ordered learning path (course names with their prerequisites
and skills gained). For each course, write ONE short reason (max ~20 words)
explaining why it fits this specific student, referencing their actual
background/current skills/interests where relevant. Then write a short
2-3 sentence overall summary of the learning path.

Do not invent skills or experience the student didn't state. Do not reorder
or add/remove courses - only explain the given path."""


def build_recommendation_prompt(
    *,
    name: str,
    background: str,
    education: str,
    career_goal: str,
    current_skills: list[str],
    interests: list[str],
    path_courses: list[dict],
) -> list[dict[str, str]]:
    courses_text = "\n".join(
        f"{i + 1}. {c['name']} (prerequisites: "
        f"{', '.join(c['prerequisites']) or 'none'}; skills gained: "
        f"{', '.join(c['skills_gained'])})"
        for i, c in enumerate(path_courses)
    )

    user_prompt = (
        f"Student name: {name}\n"
        f"Education: {education or 'n/a'}\n"
        f"Background: {background or 'n/a'}\n"
        f"Career goal: {career_goal}\n"
        f"Current skills: {', '.join(current_skills) or 'none listed'}\n"
        f"Interests: {', '.join(interests) or 'none listed'}\n\n"
        f"Learning path (already ordered - do not change the order):\n{courses_text}\n\n"
        'Respond ONLY with JSON in this exact shape:\n'
        '{"reasons": {"<course name>": "<reason>"}, "summary": "<2-3 sentence summary>"}'
    )
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ]
