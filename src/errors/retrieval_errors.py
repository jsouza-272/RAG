from .rag_error import RagError


class RetrivalError(RagError):
    """
    RetrievalError is a custom exception class that inherits from RagError.

    This exception is raised when there is an error related to data retrieval.

    Attributes:
        msg (str): A message describing the error.

    Args:
        msg (str): A string message that provides details about the
        retrieval error.
    """

    def __init__(self, msg: str) -> None:
        """
        Initialize a RetrievalError instance.

        Args:
            msg (str): The error message to be displayed.
        """

        super().__init__(f"RetrivalError: {msg}")
