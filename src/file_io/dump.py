import os
import json
from pathlib import Path
from src.errors import DumpError
from src.models import (
    MinimalSource, StudentSearchResults,
    StudentSearchResultsAndAnswer
    )


def dump_chunks(chunks: list[MinimalSource], output_file: str) -> None:
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
