import json
from pydantic import ValidationError
from pathlib import Path
from src.errors import LoadError
from src.models import MinimalSource, RagDataset, StudentSearchResults


def load_chunk(chunk_file: Path) -> list[MinimalSource]:
    """
    Load a chunk of data from a specified JSON file.

    This function reads a JSON file containing chunk data and converts it into
    a list of `MinimalSource` objects.
    If the file does not exist or contains invalid JSON,
    appropriate errors are raised.

    Args:
        chunk_file (Path): The path to the JSON file containing the chunk data.

    Returns:
        list[MinimalSource]: A list of `MinimalSource` objects created
        from the JSON data.

    Raises:
        LoadError: If the chunk file does not exist or if the JSON
        format is invalid.
    """

    if not chunk_file.exists():
        raise LoadError("Chunk file not found, run 'index' first")
    try:
        with open(chunk_file) as file:
            chunk_json = json.load(file)
        chunks = [MinimalSource(**chunk) for chunk in chunk_json]
    except (json.JSONDecodeError, ValidationError):
        raise LoadError("Invalid json format")
    return chunks


def load_dataset(dataset_path: Path) -> RagDataset:
    """
    Loads a dataset from a specified JSON file.

    Args:
        dataset_path (Path): The path to the JSON file containing the dataset.

    Returns:
        RagDataset: An instance of RagDataset populated with the data from
        the JSON file.

    Raises:
        LoadError: If the JSON file is invalid or cannot be decoded.
    """

    try:
        with open(dataset_path) as file:
            return RagDataset(**json.load(file))
    except (ValidationError, json.JSONDecodeError):
        raise LoadError("Invalid json format")


def load_student_search_results(student_search_results_path: Path
                                ) -> StudentSearchResults:
    """
    Load student search results from a JSON file.

    Args:
        student_search_results_path (Path): The path to the JSON file
        containing student search results.

    Returns:
        StudentSearchResults: An instance of StudentSearchResults populated
        with data from the JSON file.

    Raises:
        LoadError: If the JSON file is invalid or cannot be decoded.
    """

    try:
        with open(student_search_results_path) as file:
            return StudentSearchResults(**json.load(file))
    except (ValidationError, json.JSONDecodeError):
        raise LoadError("Invalid json format")
