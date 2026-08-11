"""
Maps a free-text career goal to a target ordered list of catalogue course
ids. Kept as structured data (not LLM output) so the same goal always
produces the same target skill path - the LLM is only used later to write
the human-facing reasons/summary.
"""

# Each path is already listed in a prerequisite-respecting order.
CAREER_PATHS: dict[str, list[str]] = {
    "frontend_developer": ["html", "css", "javascript", "react", "typescript"],
    "backend_developer": ["python", "git", "fastapi", "postgresql"],
    "full_stack_developer": [
        "html",
        "css",
        "javascript",
        "react",
        "typescript",
        "nodejs",
        "postgresql",
    ],
    "python_developer": ["python", "git", "fastapi", "postgresql"],
    "data_scientist": [
        "python",
        "numpy-pandas",
        "data-viz",
        "machine-learning",
    ],
    "ai_ml_engineer": [
        "python",
        "numpy-pandas",
        "machine-learning",
        "deep-learning",
    ],
}

# Keyword aliases used to match a free-text career goal to a path above.
# Checked as case-insensitive substrings against the goal text.
PATH_ALIASES: dict[str, list[str]] = {
    "frontend_developer": ["frontend", "front-end", "front end", "ui developer"],
    "backend_developer": ["backend", "back-end", "back end", "api developer"],
    "full_stack_developer": ["full stack", "full-stack", "fullstack"],
    "python_developer": ["python developer", "python engineer"],
    "data_scientist": ["data scientist", "data science", "data analyst"],
    "ai_ml_engineer": [
        "machine learning",
        "ml engineer",
        "ai engineer",
        "ai/ml",
        "artificial intelligence",
        "deep learning",
    ],
}

DEFAULT_PATH_KEY = "full_stack_developer"


def match_career_path(career_goal: str) -> str:
    """Return the best-matching path key for a free-text career goal.

    Falls back to the default (full-stack) path if nothing matches, which
    is a reasonable general-purpose beginner path.
    """
    goal_lower = career_goal.lower().strip()
    if not goal_lower:
        return DEFAULT_PATH_KEY

    for path_key, aliases in PATH_ALIASES.items():
        if any(alias in goal_lower for alias in aliases):
            return path_key

    return DEFAULT_PATH_KEY
