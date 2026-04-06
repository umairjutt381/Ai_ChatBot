import re
from collections import Counter

STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "how",
    "in",
    "is",
    "it",
    "of",
    "on",
    "or",
    "that",
    "the",
    "this",
    "to",
    "was",
    "what",
    "when",
    "where",
    "which",
    "who",
    "why",
    "with",
}


def _tokenize(text: str) -> list[str]:
    words = re.findall(r"[a-zA-Z0-9']+", text.lower())
    return [word for word in words if word not in STOP_WORDS]


def answer_with_context(question: str, chunks: list[str]) -> str:
    if not chunks:
        return "I cannot answer yet because no document content is available."

    question_tokens = _tokenize(question)
    if not question_tokens:
        return "Please ask a more specific question."

    scores = []
    token_counter = Counter(question_tokens)
    for chunk in chunks:
        chunk_tokens = _tokenize(chunk)
        overlap = sum(min(token_counter[token], chunk_tokens.count(token)) for token in token_counter)
        scores.append((overlap, chunk))

    best_score, best_chunk = max(scores, key=lambda item: item[0])
    if best_score == 0:
        preview = chunks[0][:400].strip()
        return f"I could not find an exact match. Here is the most relevant context I have:\n{preview}"

    return best_chunk[:700].strip()

