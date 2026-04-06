from dataclasses import dataclass

from .llm import answer_with_context


@dataclass
class LocalQAChain:
    chunks: list[str]

    def run(self, question: str) -> str:
        return answer_with_context(question=question, chunks=self.chunks)


def build_qa_chain(vector_store: dict) -> LocalQAChain:
    chunks = vector_store.get("chunks", []) if vector_store else []
    return LocalQAChain(chunks=chunks)
