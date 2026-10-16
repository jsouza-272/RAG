class DumpError(Exception):
    def __init__(self, msg: str) -> None:
        super().__init__(f"DumpError: {msg}")
