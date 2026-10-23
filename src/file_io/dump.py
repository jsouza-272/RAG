import os
import json
from pathlib import Path
from src.errors import DumpError
from src.models import (
    MinimalSource, StudentSearchResults,
    StudentSearchResultsAndAnswer
    )


def dump_chunks(chunks: list[MinimalSource], output_file: str) -> None:
    """
    Dump a list of MinimalSource chunks to a specified output file in JSON
    format.

    Args:
        chunks (list[MinimalSource]): A list of MinimalSource objects
        to be dumped.
        output_file (str): The path to the output file where the JSON
        data will be written.

    Raises:
        DumpError: If the output file exists but is not writable,
        or if the directory for the output file cannot be created.

    Returns:
        None
    """

    output = Path(output_file)
    if output.exists():
        if os.access(output, os.W_OK):
            with open(output, mode="w") as file:
                json.dump([c.model_dump(mode='json') for c in chunks], file,
                          indent=4)
        else:
            raise DumpError(
                f"Cannot write results to '{output_file}': "
                "directory missing or not writable."
            )
    else:
        output.parent.mkdir(mode=0o775, parents=True, exist_ok=True)
        with open(output, mode="w") as file:
            json.dump([c.model_dump(mode='json') for c in chunks], file,
                      indent=4)


def dump_search_results(results: StudentSearchResults,
                        save_dir: Path, dataset: Path) -> None:
    """
    Dump search results to a specified directory.

    This function takes the search results from a `StudentSearchResults`
    object and saves them as a JSON file in the specified directory.
    If the file already exists, it checks for write permissions before
    attempting to overwrite it. If the directory does not exist,
    it creates the necessary directories with appropriate permissions.

    Args:
        results (StudentSearchResults): The search results to be dumped.
        save_dir (Path): The directory where the results will be saved.
        dataset (Path): The path object representing the dataset name used for
        the output file.

    Raises:
        DumpError: If the file already exists and is not writable,
        or if there is an issue creating the directory.
    """

    save_path = save_dir / dataset.name
    if save_path.exists():
        if os.access(save_path, os.W_OK):
            with open(save_path, mode="w") as file:
                json.dump(results.model_dump(mode="json"), file, indent=4)
        else:
            raise DumpError(
                f"Cannot write results to '{save_path}': "
                "directory missing or not writable."
            )
    else:
        save_path.parent.mkdir(mode=0o775, parents=True, exist_ok=True)
        with open(save_path, mode="w") as file:
            json.dump(results.model_dump(mode="json"), file, indent=4)


def dump_student_answers(dataset_answers: StudentSearchResultsAndAnswer,
                         save_dir: Path, dataset: Path) -> None:
    """
    Dump student answers to a specified directory.

    This function saves the student answers from the provided dataset
    to a JSON file in the specified directory.
    If the file already exists and is writable,
    it will overwrite the existing file. If the
    file does not exist, it will create the necessary directories.

    Args:
        dataset_answers (StudentSearchResultsAndAnswer): The student answers
        to be dumped, encapsulated in a data structure.
        save_dir (Path): The directory where the JSON file will be saved.
        dataset (Path): The path of the dataset, used to name the output file.

    Raises:
        DumpError: If the specified save path exists but is not writable, or
        if there is an issue creating the necessary directories.
    """

    save_path = save_dir / dataset.name
    if save_path.exists():
        if os.access(save_path, os.W_OK):
            with open(save_path, mode="w") as file:
                json.dump(dataset_answers.model_dump(mode="json"),
                          file, indent=4)
        else:
            raise DumpError(
                f"Cannot write results to '{save_path}': "
                "directory missing or not writable."
            )
    else:
        save_path.parent.mkdir(mode=0o775, parents=True, exist_ok=True)
        with open(save_path, mode="w") as file:
            json.dump(dataset_answers.model_dump(mode="json"), file, indent=4)
