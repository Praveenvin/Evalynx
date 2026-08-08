import re
from dataclasses import dataclass


@dataclass
class DocumentChunk:
    text: str
    section: str
    chunk_id: int


# Common resume section headings.
SECTION_PATTERNS = {
    "SUMMARY": [
        "summary",
        "professional summary",
        "profile",
        "objective",
        "career objective",
    ],
    "SKILLS": [
        "skills",
        "technical skills",
        "core skills",
        "technical expertise",
    ],
    "EXPERIENCE": [
        "experience",
        "work experience",
        "professional experience",
        "employment",
        "work history",
    ],
    "EDUCATION": [
        "education",
        "academic background",
        "academic qualifications",
    ],
    "PROJECTS": [
        "projects",
        "personal projects",
        "academic projects",
        "key projects",
    ],
    "CERTIFICATIONS": [
        "certifications",
        "certificates",
        "licenses & certifications",
    ],
    "ACHIEVEMENTS": [
        "achievements",
        "awards",
        "honors",
    ],
}


def normalize_heading(line: str) -> str:
    """Normalize a potential section heading."""
    line = line.strip().lower()

    # Remove common bullet characters.
    line = re.sub(r"^[•●▪◦\-–—*]+\s*", "", line)

    # Remove trailing punctuation.
    line = line.rstrip(":").strip()

    return line


def detect_section(line: str) -> str | None:
    """Detect common resume section headings despite PDF artifacts."""

    original = line.strip()

    if not original:
        return None

    candidates = [original]

    # Remove leading non-ASCII/symbol artifacts.
    cleaned = re.sub(r"^[^A-Za-z]+", "", original).strip()

    if cleaned != original:
        candidates.append(cleaned)

    # Some PDF extractors produce a single lowercase artifact
    # before uppercase headings, e.g. "l EXPERIENCE".
    cleaned_without_prefix = re.sub(
        r"^[a-z]\s+(?=[A-Z])",
        "",
        cleaned,
    ).strip()

    if cleaned_without_prefix != cleaned:
        candidates.append(cleaned_without_prefix)

    for candidate in candidates:
        normalized = normalize_heading(candidate)

        for section, patterns in SECTION_PATTERNS.items():
            if normalized in patterns:
                return section

    return None


def split_into_sections(text: str) -> list[tuple[str, str]]:
    """
    Split resume text into logical sections.

    Returns:
        [(section_name, section_text), ...]
    """

    lines = text.splitlines()

    sections: list[tuple[str, str]] = []

    current_section = "GENERAL"
    current_lines: list[str] = []

    for line in lines:
        section = detect_section(line)

        if section:
            if current_lines:
                section_text = "\n".join(current_lines).strip()

                if section_text:
                    sections.append((current_section, section_text))

            current_section = section
            current_lines = []
        else:
            current_lines.append(line)

    # Add final section.
    if current_lines:
        section_text = "\n".join(current_lines).strip()

        if section_text:
            sections.append((current_section, section_text))

    return sections


def create_chunks(
    text: str,
    max_chunk_size: int = 1200,
) -> list[DocumentChunk]:
    """
    Create section-aware chunks from resume text.

    Sections are preserved whenever possible.
    Large sections are split into smaller chunks.
    """

    sections = split_into_sections(text)

    chunks: list[DocumentChunk] = []
    chunk_id = 0

    for section_name, section_text in sections:

        # If the entire section fits, keep it as one chunk.
        if len(section_text) <= max_chunk_size:
            chunks.append(
                DocumentChunk(
                    text=section_text,
                    section=section_name,
                    chunk_id=chunk_id,
                )
            )

            chunk_id += 1
            continue

        # Otherwise split the section by paragraphs.
        paragraphs = re.split(r"\n\s*\n", section_text)

        current_chunk = ""

        for paragraph in paragraphs:
            paragraph = paragraph.strip()

            if not paragraph:
                continue

            # If adding the paragraph exceeds the limit,
            # save the current chunk first.
            if (
                current_chunk
                and len(current_chunk) + len(paragraph) + 2
                > max_chunk_size
            ):
                chunks.append(
                    DocumentChunk(
                        text=current_chunk.strip(),
                        section=section_name,
                        chunk_id=chunk_id,
                    )
                )

                chunk_id += 1
                current_chunk = ""

            current_chunk += paragraph + "\n\n"

        # Save remaining content.
        if current_chunk.strip():
            chunks.append(
                DocumentChunk(
                    text=current_chunk.strip(),
                    section=section_name,
                    chunk_id=chunk_id,
                )
            )

            chunk_id += 1

    return chunks