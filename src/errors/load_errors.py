from .rag_error import RagError


class LoadError(RagError):
    """
    LoadError is a custom exception class that inherits from RagError.

    This exception is raised when there is an error related to
    loading operations.

    Attributes:
        msg (str): A message describing the error.

    Args:
        msg (str): A string message that provides details about the load error.
    """

    def __init__(self, msg: str) -> None:
        super().__init__(f"LoadError: {msg}")
