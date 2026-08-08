from app.services.rag.document_loader import extract_text


file_path = "data/atsresume.pdf"

text = extract_text(file_path)

print("----- EXTRACTED TEXT -----")
print(text)
