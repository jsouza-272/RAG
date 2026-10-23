from .rag_error import RagError


class DumpError(RagError):
    """
    Class representing an error that occurs during a dump operation.

    This class inherits from the RagError base class and is initialized with
    a message
    that describes the specific dump error.

    Attributes:
        msg (str): The error message associated with the dump error.

    Args:
        msg (str): A string containing the error message to be displayed.
    """

    def __init__(self, msg: str) -> None:
        """
        Initialize a DumpError instance.

        Args:
            msg (str): The error message to be included in the exception.
        """

        super().__init__(f"DumpError: {msg}")
