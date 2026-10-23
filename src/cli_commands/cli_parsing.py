import json
from tempfile import TemporaryFile
from pathlib import Path
from src.models import RagDataset, StudentSearchResults
from pydantic import ValidationError
from src.errors import (
    TopKError, MaxChunkSizeError, DataSetPathError,
    SaveDirectoryError, QueryError, StudentSearchResultsPathError
    )


def parse_k(k: int = 5) -> int:
    """
    Parse the value of k.

    This function validates the input k to ensure it is a positive integer.
    If k is not an integer or is a boolean, or if it is less than or equal
    to zero,
    a TopKError is raised.

    Args:
        k (int, optional): The value to be parsed. Defaults to 5.

    Returns:
        int: The validated positive integer k.

    Raises:
        TopKError: If k is not an integer, is a boolean, or is less than or
        equal to zero.
    """

    if not isinstance(k, int) or isinstance(k, bool):
        raise TopKError("k must be an integer,"
                        f" got {k!r} ({type(k).__name__})")
    if k <= 0:
        raise TopKError(f"k must be a positive integer (k > 0), got {k}")
    return k


def parse_max_chunk_size(max_chunk_size: int = 2000) -> int:
    """
    Parse the maximum chunk size.

    This function validates the provided maximum chunk size and ensures
    it adheres to specified constraints.
    If the input is not a valid integer or is a boolean, it raises
    a `TopKError`.
    If the input is less than 500, it raises a `MaxChunkSizeError`.
    If the input exceeds 2000, it returns 2000; otherwise, it returns the
    input value.

    Args:
        max_chunk_size (int, optional): The maximum chunk size to parse.
        Defaults to 2000.

    Returns:
        int: The validated maximum chunk size, capped at 2000.

    Raises:
        TopKError: If `max_chunk_size` is not an integer or is a boolean.
        MaxChunkSizeError: If `max_chunk_size` is less than 500.
    """

    if (not isinstance(max_chunk_size, int)
            or isinstance(max_chunk_size, bool)):
        raise TopKError("k must be an integer,"
                        f" got {max_chunk_size!r} "
                        f"({type(max_chunk_size).__name__})")
    if max_chunk_size < 500:
        raise MaxChunkSizeError("max_chunk_size must be at "
                                f"least 500, got {max_chunk_size}")
    if max_chunk_size > 2000:
        return 2000
    return max_chunk_size


def parse_dataset_path(dataset_path: str) -> Path:
    """
    Parse the dataset path and validate its properties.

    This function checks if the provided dataset path is a valid string,
    ensures it is not empty, verifies that it ends with a '.json' extension,
    and checks if the file exists and is readable.
    It also attempts to load the JSON content and validate it
    against the expected structure for a RagDataset.

    Args:
        dataset_path (str): The path to the dataset file.

    Returns:
        Path: A Path object representing the validated dataset path.

    Raises:
        DataSetPathError: If the dataset_path is not a string, is empty,
        does not end with '.json', does not exist, is not readable,
        or contains invalid JSON or a malformed RagDataset.
    """

    if not isinstance(dataset_path, str):
        raise DataSetPathError("dataset_path must be a string, "
                               f"got {dataset_path!r} "
                               f"({type(dataset_path).__name__})")
    if not dataset_path:
        raise DataSetPathError("dataset_path must not be empty")
    if not dataset_path.endswith(".json"):
        raise DataSetPathError("dataset_path must be a "
                               f".json file, got {dataset_path!r}")
    dataset = Path(dataset_path)
    if not dataset.exists():
        raise DataSetPathError("dataset_path must be an "
                               f"existing file, got {dataset_path!r}")
    try:
        with open(dataset) as file:
            RagDataset(**json.load(file))
    except json.JSONDecodeError as error:
        raise DataSetPathError("dataset_path must contain valid "
                               f"JSON, got {dataset_path!r} ({error.msg})"
                               )
    except PermissionError:
        raise DataSetPathError("dataset_path must be readable, "
                               f"got {dataset_path!r} (permission denied)")
    except ValidationError as error:
        loc = error.errors()[0]["loc"][0]
        typ = error.errors()[0]["type"]
        raise DataSetPathError("dataset_path must contain a valid RagDataset, "
                               f"got {dataset_path!r} ({typ} {loc})")
    return dataset


def parse_save_directory(save_directory: str) -> Path:
    """
    Parse and validate the specified save directory.

    This function checks if the provided save directory is a valid string,
    ensures that it does not contain a file extension, verifies that
    it exists as a directory, and checks for write permissions.

    Args:
        save_directory (str): The path to the save directory.

    Returns:
        Path: A Path object representing the validated save directory.

    Raises:
        SaveDirectoryError: If the save_directory is not a string, contains a
        file extension, does not exist as a directory, or is not writable.
    """

    if not isinstance(save_directory, str):
        raise SaveDirectoryError("save_directory must be a string, "
                                 f"got {save_directory!r} "
                                 f"({type(save_directory).__name__})")
    save_dir = Path(save_directory)
    if save_dir.suffix:
        raise SaveDirectoryError("save_directory name must not contain '.', "
                                 f"got {save_directory!r}")
    if save_dir.exists():
        if not save_dir.is_dir():
            raise SaveDirectoryError("save_directory must be a directory, "
                                     f"got {save_directory!r} "
                                     "(path exists but is not a directory)")
        try:
            with TemporaryFile(dir=save_dir):
                pass
        except PermissionError:
            raise SaveDirectoryError("save_directory must be writable, got "
                                     f"{save_directory!r} (permission denied)"
                                     )
    return save_dir


def parse_query(query: str) -> str:
    """
    Parse a query string and validate its content.

    This function checks if the provided query is a non-empty string that
    contains at least one alphanumeric character.
    If the query does not meet these criteria,
    a QueryError is raised with an appropriate message.

    Args:
        query (str): The query string to be parsed and validated.

    Returns:
        str: The validated query string.

    Raises:
        QueryError: If the query is not a string, is empty, or contains only
        whitespace or non-alphanumeric characters.
    """

    if not isinstance(query, str):
        raise QueryError("query must be a string, got "
                         f"{query!r} ({type(query).__name__})")
    if not query:
        raise QueryError("query must not be empty")
    if all(c.isspace() or not c.isalnum() for c in query):
        raise QueryError("query must contain at least one "
                         f"letter or digit, got {query!r}")
    return query


def parse_student_search_results_path(
        student_search_results_path: str) -> Path:
    """
    Parse the student search results file path and validate its contents.

    This function checks if the provided path is a valid string, ensures it
    points to a non-empty `.json` file, verifies that the file exists,
    and checks that it contains valid JSON data. If any of these conditions
    are not met,
    a `StudentSearchResultsPathError` is raised with an appropriate message.

    Args:
        student_search_results_path (str): The path to the student search
        results file.

    Returns:
        Path: A `Path` object representing the validated student search
        results file.

    Raises:
        StudentSearchResultsPathError: If the provided path is not a string,
        is empty, does not end with `.json`, does not exist, is not readable,
        or does not contain valid JSON data.
    """

    if not isinstance(student_search_results_path, str):
        raise StudentSearchResultsPathError(
            "student_search_results_path must be a string, "
            f"got {student_search_results_path!r} "
            f"({type(student_search_results_path).__name__})"
            )
    if not student_search_results_path:
        raise StudentSearchResultsPathError(
            "student_search_results_path must not be empty")

    if not student_search_results_path.endswith(".json"):
        raise StudentSearchResultsPathError(
            "student_search_results_path must be a "
            f".json file, got {student_search_results_path!r}")

    student_search_results = Path(student_search_results_path)
    if not student_search_results.exists():
        raise StudentSearchResultsPathError(
            "student_search_results_path must be an "
            f"existing file, got {student_search_results_path!r}")
    try:
        with open(student_search_results) as file:
            StudentSearchResults(**json.load(file))
    except json.JSONDecodeError as error:
        raise StudentSearchResultsPathError(
            "student_search_results_path must contain valid "
            f"JSON, got {student_search_results_path!r} ({error.msg})"
                                )

    except PermissionError:
        raise StudentSearchResultsPathError(
            "student_search_results_path must be readable, "
            f"got {student_search_results_path!r} (permission denied)")

    except ValidationError as error:
        loc = error.errors()[0]["loc"][0]
        typ = error.errors()[0]["type"]
        raise StudentSearchResultsPathError(
            "student_search_results_path must contain a valid RagDataset, "
            f"got {student_search_results_path!r} ({typ} {loc})")

    return student_search_results
