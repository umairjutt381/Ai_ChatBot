from pathlib import Path


def _load_pdf_text(file_path: str) -> str:
    try:
        from pypdf import PdfReader
    except Exception:
        return ""

    text_parts = []
    reader = PdfReader(file_path)
    for page in reader.pages:
        text_parts.append(page.extract_text() or "")
    return "\n".join(text_parts).strip()


def load_document(file_path: str) -> str:
    path = Path(file_path)
    suffix = path.suffix.lower()

    if suffix == ".pdf":
        pdf_text = _load_pdf_text(file_path)
        if pdf_text:
            return pdf_text

    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="latin-1", errors="ignore")
