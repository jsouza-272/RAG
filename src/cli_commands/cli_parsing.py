import json
from tempfile import TemporaryFile
from pathlib import Path
from src.models import RagDataset
from pydantic import ValidationError
from src.errors import (
    TopKError, MaxChunkSizeError, DataSetPathError,
    SaveDirectoryError, QueryError, StudentSearchResultsPathError
    )


def parse_k(k: int = 5) -> int:
    if not isinstance(k, int) or isinstance(k, bool):
        raise TopKError("k must be an integer,"
                        f" got {k!r} ({type(k).__name__})")
    if k <= 0:
        raise TopKError(f"k must be a positive integer (k > 0), got {k}")
    return k


def parse_max_chunk_size(max_chunk_size: int = 2000) -> int:
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
    if not isinstance(query, str):
        raise QueryError("query must be a string, got "
                         f"{query!r} ({type(query).__name__})")
    if not query:
        raise QueryError("query must not be empty")
    if all(c.isspace() or not c.isalnum() for c in query):
        raise QueryError("query must contain at least one "
                         f"letter or digit, got {query!r}")
    return query


def parse_student_search_results_path(student_search_results_path: str):
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
            RagDataset(**json.load(file))
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
