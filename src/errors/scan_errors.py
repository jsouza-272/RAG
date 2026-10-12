class ScanError(Exception):
    def __init__(self, msg: str = "") -> None:
        super().__init__(f"ScanError: {msg}")


class InvalidFileTypeError(ScanError):
    def __init__(self, msg: str = "") -> None:
        super().__init__(msg)
