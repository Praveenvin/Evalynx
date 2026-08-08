from app.services.rag.document_loader import extract_text
from app.services.rag.chunker import create_chunks


file_path = "data/atsresume.pdf"

text = extract_text(file_path)
chunks = create_chunks(text)

print(f"\nTotal chunks: {len(chunks)}\n")

for chunk in chunks:
    preview = chunk.text.replace("\n", " ")[:120]

    print(
        f"Chunk {chunk.chunk_id:02d} | "
        f"Section: {chunk.section:<15} | "
        f"Length: {len(chunk.text):4d} | "
        f"{preview}..."
    )