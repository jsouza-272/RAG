from .rag_error import RagError


class EvaluateError(RagError):
    def __init__(self, msg: str) -> None:
        super().__init__(f"EvaluateError: {msg}")
