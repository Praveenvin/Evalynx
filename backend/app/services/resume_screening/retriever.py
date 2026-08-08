from app.services.rag.embeddings import embedding_service
from app.services.rag.vector_store import FAISSVectorStore
from app.services.resume_screening.candidate import Candidate


class CandidateRetriever:
    def __init__(self):
        self.embedding_service = embedding_service

    def retrieve(
        self,
        candidate: Candidate,
        job_description: str,
        top_k: int = 5,
    ) -> list[dict]:

        if not candidate.chunks:
            return []

        chunk_texts = [
            chunk.text
            for chunk in candidate.chunks
        ]

        embeddings = self.embedding_service.encode(
            chunk_texts
        )

        metadata = [
            {
                "chunk_id": chunk.chunk_id,
                "section": chunk.section,
                "text": chunk.text,
                "candidate_id": candidate.candidate_id,
                "filename": candidate.filename,
            }
            for chunk in candidate.chunks
        ]

        vector_store = FAISSVectorStore(
            dimension=embeddings.shape[1]
        )

        vector_store.add(
            embeddings,
            metadata,
        )

        query_embedding = self.embedding_service.encode(
            [job_description]
        )[0]

        results = vector_store.search(
            query_embedding,
            top_k=top_k,
        )

        candidate.retrieved_evidence = results

        return results