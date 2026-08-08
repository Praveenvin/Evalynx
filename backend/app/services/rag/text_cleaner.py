import re


def clean_text(text: str) -> str:
    """
    Clean PDF/DOCX extracted text while preserving
    meaningful resume content.
    """

    # Normalize line endings
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Fix words broken across lines.
    # Example: "Post-\nGreSQL" -> "PostGreSQL"
    text = re.sub(r"(?<=\w)-\n(?=\w)", "", text)

    # Normalize common bullet characters
    text = re.sub(r"[•●▪◦]", "•", text)

    # Remove isolated PDF encoding artifacts.
    # IMPORTANT: only remove them when they appear as
    # standalone characters, never from inside words.
    text = re.sub(r"(?m)^[ \t]*[Ðõ§{jz][ \t]+", "", text)

    # Remove isolated artifact symbols appearing before headings.
    text = re.sub(r"(?m)^[ \t]*[^\w\s•#()+&/.-][ \t]+(?=[A-Z])", "", text)

    # Remove markdown-style links while preserving visible text.
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)

    # Remove excessive whitespace around newlines
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n[ \t]+", "\n", text)

    # Collapse excessive blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Collapse repeated spaces
    text = re.sub(r"[ \t]{2,}", " ", text)

    return text.strip()