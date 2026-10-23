from .rag_error import RagError


class DumpError(RagError):
    def __init__(self, msg: str) -> None:
        super().__init__(f"DumpError: {msg}")
