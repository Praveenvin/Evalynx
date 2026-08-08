def get_recommendation(score: float) -> str:
    if score >= 80:
        return "Strong Match"

    if score >= 65:
        return "Good Match"

    if score >= 50:
        return "Potential Match"

    return "Weak Match"


def calculate_final_score(
    llm_evaluation: dict,
    retrieved_evidence: list[dict],
) -> dict:
    """
    Combine LLM evaluation scores with semantic
    retrieval relevance.

    Final score:
        35% Skills
        30% Experience
        15% Education
        20% Semantic Relevance
    """

    skills_score = float(
        llm_evaluation.get("skills_score", 0)
    )

    experience_score = float(
        llm_evaluation.get("experience_score", 0)
    )

    education_score = float(
        llm_evaluation.get("education_score", 0)
    )

    semantic_score = calculate_semantic_score(
        retrieved_evidence
    )

    final_score = (
        skills_score * 0.35
        + experience_score * 0.30
        + education_score * 0.15
        + semantic_score * 0.20
    )

    recommendation = get_recommendation(
        final_score
    )

    return {
        "overall_score": round(
            final_score,
            2,
        ),
        "skills_score": round(
            skills_score,
            2,
        ),
        "experience_score": round(
            experience_score,
            2,
        ),
        "education_score": round(
            education_score,
            2,
        ),
        "semantic_score": round(
            semantic_score,
            2,
        ),
        "strengths": llm_evaluation.get(
            "strengths",
            [],
        ),
        "gaps": llm_evaluation.get(
            "gaps",
            [],
        ),
        "recommendation": recommendation,
    }


def calculate_semantic_score(
    retrieved_evidence: list[dict],
) -> float:
    """
    Convert FAISS cosine similarity into a
    0-100 semantic relevance score.
    """

    if not retrieved_evidence:
        return 0.0

    scores = [
        float(item["score"])
        for item in retrieved_evidence
    ]

    best_score = max(scores)

    normalized = (
        best_score + 1
    ) / 2

    return normalized * 100