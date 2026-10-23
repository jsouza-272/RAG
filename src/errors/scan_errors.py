from .rag_error import RagError


class ScanError(RagError):
    """
    Class representing an error that occurs during a scan operation.

    This class inherits from the RagError base class and is used to indicate
    specific issues encountered while scanning.

    Attributes:
        msg (str): A message describing the error.

    Methods:
        __init__(msg: str): Initializes the ScanError with a specific
        error message.
    """

    def __init__(self, msg: str = "") -> None:
        """
        Initializes a ScanError instance.

        Args:
            msg (str, optional): The error message to be included in the
            exception. Defaults to an empty string.
        """

        super().__init__(f"ScanError: {msg}")


class InvalidFileTypeError(ScanError):
    """
    Class representing an error for invalid file types.

    This class inherits from the ScanError base class and is used to indicate
    that an operation has been attempted on a file type that is not supported.

    Attributes:
        msg (str): A message describing the error. Defaults to an empty string.

    Methods:
        __init__(msg: str = ""): Initializes a new instance of
        InvalidFileTypeError.
    """

    def __init__(self, msg: str = "") -> None:
        """
        Initialize a new instance of the class.

        Args:
            msg (str, optional): A message to initialize the instance with.
            Defaults to an empty string.
        """

        super().__init__(msg)
