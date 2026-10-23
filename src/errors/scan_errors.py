from .rag_error import RagError


class ScanError(RagError):
    def __init__(self, msg: str = "") -> None:
        super().__init__(f"ScanError: {msg}")


class InvalidFileTypeError(ScanError):
    def __init__(self, msg: str = "") -> None:
        super().__init__(msg)
