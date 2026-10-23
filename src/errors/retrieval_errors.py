from .rag_error import RagError


class RetrivalError(RagError):
    def __init__(self, msg: str) -> None:
        super().__init__(f"RetrivalError: {msg}")
