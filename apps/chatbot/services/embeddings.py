def get_embeddings() -> dict:
    """Return local embedding config placeholder for future model integration."""
    return {"provider": "local", "type": "keyword-overlap"}
