import numpy as np

from app.services.rag.embeddings import embedding_service


def cosine_similarity(
    query_embedding: np.ndarray,
    document_embeddings: np.ndarray,
) -> np.ndarray:
    """
    Calculate cosine similarity between one query vector
    and multiple document vectors.

    Embeddings are already normalized, so dot product
    is equivalent to cosine similarity.
    """

    return np.dot(document_embeddings, query_embedding)


def rank_chunks_by_similarity(
    query: str,
    chunks,
    top_k: int = 5,
):
    """
    Rank document chunks according to their semantic
    similarity with the query.
    """

    query_embedding = embedding_service.encode([query])[0]

    chunk_texts = [chunk.text for chunk in chunks]

    chunk_embeddings = embedding_service.encode(chunk_texts)

    scores = cosine_similarity(
        query_embedding,
        chunk_embeddings,
    )

    ranked_indices = np.argsort(scores)[::-1][:top_k]

    results = []

    for index in ranked_indices:
        chunk = chunks[index]

        results.append(
            {
                "chunk_id": chunk.chunk_id,
                "section": chunk.section,
                "score": float(scores[index]),
                "text": chunk.text,
            }
        )

    return results