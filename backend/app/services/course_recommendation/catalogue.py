"""
Static, in-memory course/skill catalogue for the Course Recommendation agent.

No database yet - this is intentionally structured application data (not
LLM-generated) so recommendations stay deterministic and explainable. The
LLM is only used to phrase the "reason" and "summary" text - see
recommendation_service.py.
"""
from dataclasses import dataclass, field


@dataclass
class Course:
    id: str
    name: str
    description: str
    category: str
    difficulty: str  # "Beginner" | "Intermediate" | "Advanced"
    prerequisites: list[str] = field(default_factory=list)  # course ids
    duration: str = ""
    skills_gained: list[str] = field(default_factory=list)


CATALOGUE: list[Course] = [
    Course(
        id="html",
        name="HTML",
        description="Structure web pages with semantic HTML markup.",
        category="Frontend Development",
        difficulty="Beginner",
        prerequisites=[],
        duration="1 week",
        skills_gained=["HTML"],
    ),
    Course(
        id="css",
        name="CSS",
        description="Style and lay out web pages, including responsive design.",
        category="Frontend Development",
        difficulty="Beginner",
        prerequisites=["html"],
        duration="1-2 weeks",
        skills_gained=["CSS"],
    ),
    Course(
        id="javascript",
        name="JavaScript",
        description="Core programming language for interactive, dynamic web pages.",
        category="Frontend Development",
        difficulty="Beginner",
        prerequisites=["css"],
        duration="3-4 weeks",
        skills_gained=["JavaScript"],
    ),
    Course(
        id="git",
        name="Git & Version Control",
        description="Track changes and collaborate on code using Git and GitHub.",
        category="Full Stack Development",
        difficulty="Beginner",
        prerequisites=[],
        duration="3-4 days",
        skills_gained=["Git", "GitHub"],
    ),
    Course(
        id="react",
        name="React",
        description="Build component-based, interactive user interfaces with React.",
        category="Frontend Development",
        difficulty="Intermediate",
        prerequisites=["javascript"],
        duration="3-4 weeks",
        skills_gained=["React"],
    ),
    Course(
        id="typescript",
        name="TypeScript",
        description="Add static typing on top of JavaScript for safer, more maintainable code.",
        category="Frontend Development",
        difficulty="Intermediate",
        prerequisites=["javascript"],
        duration="1-2 weeks",
        skills_gained=["TypeScript"],
    ),
    Course(
        id="nodejs",
        name="Node.js",
        description="Use JavaScript on the server to build APIs and backend services.",
        category="Backend Development",
        difficulty="Intermediate",
        prerequisites=["javascript"],
        duration="2-3 weeks",
        skills_gained=["Node.js", "Express"],
    ),
    Course(
        id="postgresql",
        name="PostgreSQL",
        description="Design relational schemas and write SQL for real applications.",
        category="Backend Development",
        difficulty="Intermediate",
        prerequisites=[],
        duration="2 weeks",
        skills_gained=["PostgreSQL", "SQL"],
    ),
    Course(
        id="mongodb",
        name="MongoDB",
        description="Model and query data in a document-oriented NoSQL database.",
        category="Backend Development",
        difficulty="Intermediate",
        prerequisites=[],
        duration="1-2 weeks",
        skills_gained=["MongoDB", "NoSQL"],
    ),
    Course(
        id="python",
        name="Python",
        description="General-purpose programming fundamentals used across backend, data, and AI work.",
        category="Python Development",
        difficulty="Beginner",
        prerequisites=[],
        duration="3-4 weeks",
        skills_gained=["Python"],
    ),
    Course(
        id="fastapi",
        name="FastAPI",
        description="Build fast, typed REST APIs in Python.",
        category="Backend Development",
        difficulty="Intermediate",
        prerequisites=["python"],
        duration="2 weeks",
        skills_gained=["FastAPI", "REST APIs"],
    ),
    Course(
        id="numpy-pandas",
        name="NumPy & Pandas",
        description="Manipulate and analyze structured data efficiently in Python.",
        category="Data Science",
        difficulty="Intermediate",
        prerequisites=["python"],
        duration="2-3 weeks",
        skills_gained=["NumPy", "Pandas"],
    ),
    Course(
        id="data-viz",
        name="Data Visualization",
        description="Communicate insights clearly using Matplotlib and Seaborn.",
        category="Data Science",
        difficulty="Intermediate",
        prerequisites=["numpy-pandas"],
        duration="1-2 weeks",
        skills_gained=["Matplotlib", "Seaborn", "Data Visualization"],
    ),
    Course(
        id="machine-learning",
        name="Machine Learning",
        description="Learn core ML algorithms and how to train and evaluate models with Scikit-learn.",
        category="AI/ML",
        difficulty="Advanced",
        prerequisites=["numpy-pandas"],
        duration="4-6 weeks",
        skills_gained=["Machine Learning", "Scikit-learn"],
    ),
    Course(
        id="deep-learning",
        name="Deep Learning",
        description="Build and train neural networks for advanced prediction tasks.",
        category="AI/ML",
        difficulty="Advanced",
        prerequisites=["machine-learning"],
        duration="6-8 weeks",
        skills_gained=["Deep Learning", "Neural Networks"],
    ),
]

_BY_ID = {c.id: c for c in CATALOGUE}


def get_course(course_id: str) -> Course | None:
    return _BY_ID.get(course_id)


def get_all_courses() -> list[Course]:
    return list(CATALOGUE)
