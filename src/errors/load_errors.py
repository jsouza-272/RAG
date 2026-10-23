from .rag_error import RagError


class LoadError(RagError):
    def __init__(self, msg: str) -> None:
        super().__init__(f"LoadError: {msg}")
