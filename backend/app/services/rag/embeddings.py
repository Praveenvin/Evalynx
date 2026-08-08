from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-MiniLM-L6-v2"


class EmbeddingService:
    def __init__(self, model_name: str = MODEL_NAME):
        self.model_name = model_name
        self.model = None

    def _get_model(self):
        if self.model is None:
            self.model = SentenceTransformer(
                self.model_name,
                device="cpu",
            )
        return self.model

    def encode(self, texts: list[str]):
        model = self._get_model()

        return model.encode(
            texts,
            normalize_embeddings=True,
        )


embedding_service = EmbeddingService()