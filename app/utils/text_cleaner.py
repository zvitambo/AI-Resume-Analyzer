# Purpose


def clean_text(text: str) -> str:
    """Clean extracted text from resumes or job descriptions.

    This function normalizes whitespace, line breaks, bullets, and common PDF
    extraction artifacts to produce cleaner text for downstream parsing.

    Args:
        text: Raw extracted text.

    Returns:
        Normalized text.
    """
    import re

    if text is None:
        return ""

    cleaned = text

    # Normalize line breaks
    cleaned = cleaned.replace("\r\n", "\n").replace("\r", "\n")

    # Collapse multiple spaces/tabs to a single space
    cleaned = re.sub(r"[ \t]+", " ", cleaned)

    # Standardize common bullet characters to hyphen
    cleaned = re.sub(r"[·•›‹»]+", "-", cleaned)

    # Normalize bullets that are split across line breaks
    cleaned = re.sub(r"\s*-\s*\n", "\n- ", cleaned)

    # Collapse repeated blank lines, but keep paragraph breaks
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)

    # Trim leading/trailing whitespace on each line and the whole text
    cleaned = "\n".join(line.strip() for line in cleaned.split("\n"))
    cleaned = cleaned.strip()

    return cleaned