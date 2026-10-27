from .rag_error import RagError


class ParseError(RagError):
    """
    ParseError is a custom exception class that inherits from RagError.

    This exception is raised when there is an error in parsing an argument.

    Attributes:
        argument (str): The argument that caused the parsing error.
        msg (str): A message describing the error.

    Args:
        argument (str): The argument that triggered the parse error.
        msg (str): A message providing details about the error.
    """

    def __init__(self, argument: str, msg: str) -> None:
        """
        Initialize a ParseError instance.

        Args:
            argument (str): The argument that caused the parsing error.
            msg (str): A message describing the error.
        """

        super().__init__(f"ParseError ({argument}): {msg}")


class TopKError(ParseError):
    """
    Class representing a top-k error.

    This class inherits from the ParseError class and is used to indicate
    an error related to the top-k functionality.

    Attributes:
        msg (str): The error message associated with the top-k error.

    Methods:
        __init__(msg: str) -> None: Initializes the TopKError with a
        specific message.
    """

    def __init__(self, msg: str) -> None:
        """
        Initialize the class with a message.

        Args:
            msg (str): The message to be passed to the superclass initializer.
        """

        super().__init__("top-k", msg)


class QueryError(ParseError):
    """
    Class representing an error that occurs during a query parsing operation.

    Inherits from `ParseError` and is initialized with a specific
    error message.

    Attributes:
        msg (str): The error message associated with the query error.

    Args:
        msg (str): A message describing the query error.
    """

    def __init__(self, msg: str) -> None:
        """
        Initialize a new instance of the class.

        Args:
            msg (str): The message to be passed to the superclass initializer.
        """

        super().__init__("query", msg)


class QuestionError(ParseError):
    """
    Class representing an error related to a question.

    This class inherits from the ParseError class and is used to indicate
    specific errors that occur during the parsing of questions.

    Attributes:
        msg (str): The error message associated with the question error.

    Args:
        msg (str): A message describing the error.
    """

    def __init__(self, msg: str) -> None:
        """
        Initializes a new instance of the class.

        Args:
            msg (str): The message to be associated with the instance.
        """

        super().__init__("question", msg)


class MaxChunkSizeError(ParseError):
    """
    Class representing an error related to exceeding the maximum chunk size.

    This error is a subclass of `ParseError` and is raised when a chunk size
    exceeds the defined maximum limit.

    Attributes:
        msg (str): The error message associated with the exception.

    Args:
        msg (str): A message describing the error.
    """

    def __init__(self, msg: str) -> None:
        """
        Initialize a new instance of the class.

        Args:
            msg (str): The message to be passed to the superclass initializer.

        Returns:
            None
        """

        super().__init__("max_chunk_size", msg)


class DataSetPathError(ParseError):
    """
    Class representing an error related to dataset paths.

    This class inherits from the ParseError class and is used to indicate
    specific issues encountered when dealing with dataset paths.

    Attributes:
        msg (str): The error message associated with the dataset path error.

    Args:
        msg (str): A message describing the error.
    """

    def __init__(self, msg: str) -> None:
        """
        Initialize the class with a message.

        Args:
            msg (str): The message to be passed to the superclass initializer.
        """

        super().__init__("dataset_path", msg)


class SaveDirectoryError(ParseError):
    """
    Class representing an error related to the save directory.

    This class inherits from the ParseError class and is used to indicate
    issues specifically associated with the save directory.

    Attributes:
        msg (str): The error message describing the issue with
        the save directory.

    Methods:
        __init__(msg: str) -> None: Initializes the SaveDirectoryError
        with a specific message.
    """

    def __init__(self, msg: str) -> None:
        """
        Initialize the class with a message.

        Args:
            msg (str): The message to be passed to the superclass initializer.
        """

        super().__init__("save_directory", msg)


class StudentSearchResultsPathError(ParseError):
    """
    Class representing an error related to student search results path.

    This class inherits from the ParseError class and is used to indicate
    specific issues encountered when processing student search results paths.

    Attributes:
        msg (str): The error message associated with the exception.

    Args:
        msg (str): A message describing the error.
    """

    def __init__(self, msg: str) -> None:
        """
        Initializes a new instance of the class.

        Args:
            msg (str): A message to be passed to the superclass initializer.
        """

        super().__init__("student_search_results_path", msg)


class ArgError(ParseError):
    def __init__(self, msg: str) -> None:
        super().__init__("too many arguments", msg)
