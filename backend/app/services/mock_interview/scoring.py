"""
Final interview scores are calculated locally from the per-answer
evaluations rather than trusting a single LLM-generated overall number.
Keep the weighting here so it's easy to tune independently of prompts.
"""

TECHNICAL_WEIGHT = 0.30
COMMUNICATION_WEIGHT = 0.25
PROBLEM_SOLVING_WEIGHT = 0.25
RELEVANCE_WEIGHT = 0.20


def _average(values: list[float]) -> float:
    return round(sum(values) / len(values), 1) if values else 0.0


def calculate_final_scores(evaluations: list[dict]) -> dict:
    """Aggregate per-answer evaluation dicts into the four final categories
    plus a locally-computed overall score.
    """
    if not evaluations:
        return {
            "overall_score": 0,
            "technical_knowledge": 0,
            "communication": 0,
            "problem_solving": 0,
            "confidence_clarity": 0,
        }

    technical = _average([e.get("technical_score", 0) for e in evaluations])
    communication = _average([e.get("communication_score", 0) for e in evaluations])
    problem_solving = _average([e.get("problem_solving_score", 0) for e in evaluations])
    relevance = _average([e.get("relevance_score", 0) for e in evaluations])

    overall = (
        technical * TECHNICAL_WEIGHT
        + communication * COMMUNICATION_WEIGHT
        + problem_solving * PROBLEM_SOLVING_WEIGHT
        + relevance * RELEVANCE_WEIGHT
    )

    return {
        "overall_score": round(overall),
        "technical_knowledge": round(technical),
        "communication": round(communication),
        # "confidence / clarity" in the final UI maps to relevance+communication
        # blend since clarity is captured in communication and relevance
        # reflects how on-target (confident) the answers were.
        "problem_solving": round(problem_solving),
        "confidence_clarity": round(_average([communication, relevance])),
    }