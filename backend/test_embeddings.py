from app.services.rag.embeddings import embedding_service


texts = [
    "React developer with REST API experience",
    "Python Django backend developer",
    "Bachelor of Engineering in Computer Science",
]

embeddings = embedding_service.encode(texts)

print("Number of texts:", len(embeddings))
print("Embedding dimensions:", embeddings.shape)
print("\nFirst embedding:")
print(embeddings[0])