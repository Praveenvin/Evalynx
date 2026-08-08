import faiss
import numpy as np


class FAISSVectorStore:
    def __init__(self, dimension: int):
        self.dimension = dimension
        self.index = faiss.IndexFlatIP(dimension)
        self.metadata = []

    def add(
        self,
        embeddings: np.ndarray,
        metadata: list[dict],
    ):
        """
        Add normalized embeddings and their metadata
        to the FAISS index.
        """

        embeddings = np.asarray(
            embeddings,
            dtype="float32",
        )

        self.index.add(embeddings)

        self.metadata.extend(metadata)

    def search(
        self,
        query_embedding: np.ndarray,
        top_k: int = 5,
    ) -> list[dict]:
        """
        Search the vector index and return the
        most relevant chunks.
        """

        query_embedding = np.asarray(
            [query_embedding],
            dtype="float32",
        )

        scores, indices = self.index.search(
            query_embedding,
            top_k,
        )

        results = []

        for score, index in zip(
            scores[0],
            indices[0],
        ):
            if index == -1:
                continue

            result = self.metadata[index].copy()
            result["score"] = float(score)

            results.append(result)

        return results

    @property
    def size(self) -> int:
        return self.index.ntotal