from typing import Any

def create_vector_store(document_text: str, embeddings: Any = None) -> dict:
    chunks = [part.strip() for part in document_text.split("\n") if part.strip()]
    return {
        "chunks": chunks,
        "embeddings": embeddings,
    }
