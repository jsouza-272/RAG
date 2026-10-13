class LoadError(Exception):
    def __init__(self, msg: str) -> None:
        super().__init__(f"LoadError: {msg}")
