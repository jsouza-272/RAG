from tqdm import tqdm
from pathlib import Path
from src.errors import (
    ScanError, InvalidFileTypeError
    )
from src.consts import INVALID_PATHS


def find_files_by_suffix(dir: Path, suffix: str) -> list[Path]:
    """
    Finds all files in a directory and its subdirectories that have a
    specific suffix.

    Args:
        dir (Path): The directory to search within.
        suffix (str): The file suffix to look for (e.g., '.txt').

    Returns:
        list[Path]: A list of Paths to the files that match the specified
        suffix.
    """

    file_list: list[Path] = []
    for p in dir.iterdir():
        if p.is_file() and p.suffix == suffix:
            file_list.append(p)
        if p.is_dir():
            file_list += find_files_by_suffix(p, suffix)
    return file_list


def is_valid_dir(dir: Path) -> bool:
    """
    Checks if the given directory path is valid.

    This function verifies that the first part of the directory path is
    not in the list of invalid paths
    and that the specified path is indeed a directory.

    Args:
        dir (Path): The directory path to validate.

    Returns:
        bool: True if the directory is valid, False otherwise.
    """

    return dir.parts[0] not in INVALID_PATHS and dir.is_dir()


def find_dir_by_pattern(pattern: str, base_dir_path: str = ".") -> Path:
    """
    Find a directory by a specified pattern within a base directory.

    This function searches for directories that match a given pattern in the
    specified base directory. It raises errors if the base directory does
    not exist or is not a directory.
    If multiple directories match the pattern,
    the function will return the last one found.

    Args:
        pattern (str): The pattern to search for in directory names.
        base_dir_path (str, optional): The path to the base directory to
        search within. Defaults to the current directory (".")

    Returns:
        Path: The path of the matching directory.

    Raises:
        ScanError: If the base directory does not exist, no matching directory
        is found, or if the found path is not a directory.
        InvalidFileTypeError: If the base directory is not a directory.
    """

    base_dir = Path(base_dir_path)
    if not base_dir.exists():
        raise ScanError(
            f"base_dir does not exist, got {base_dir!r}"
            )
    if not base_dir.is_dir():
        raise InvalidFileTypeError(
            f"base_dir must be a directory, got {base_dir!r}"
        )
    cantidades_dir_list = [
        d for d in tqdm(base_dir.rglob(f"{pattern}*"),
                        "Searching for vllm", leave=False)
        if is_valid_dir(d)
    ]
    cantidades_dir_list.sort(key=lambda s: str(s))
    cantidades_dir_list.sort(key=lambda s: len(str(s)))
    dir_path = Path()
    if cantidades_dir_list:
        if len(cantidades_dir_list) > 1:
            print(
                f"multiple directories match {pattern} in '{base_dir!s}': "
                f"{[str(_) for _ in cantidades_dir_list]};"
                f" using {cantidades_dir_list[-1]!s}"
                )
        dir_path = cantidades_dir_list[-1]
    if not dir_path:
        raise ScanError(
            f"no directory matching {pattern!r} found in {base_dir!r}"
        )
    if not dir_path.is_dir():
        raise InvalidFileTypeError(
            f"{pattern!r} matched {dir_path!r}, but it is not a directory"
        )
    return dir_path


def valid_txt_parents(vllm_path: Path | None = None) -> list[Path]:
    """
    Determine valid parent directories for VLLM.

    This function checks if a specified path is provided. If not,
    it attempts to find a directory matching the pattern "vllm-".
    It then asserts that a valid path has been found and returns a list
    containing the path and its "requirements" subdirectory.

    Args:
        vllm_path (Path | None): The path to check. If None, the function will
        search for a directory matching the pattern.

    Returns:
        list[Path]: A list containing the valid VLLM path and its
        "requirements" subdirectory.
    """

    if not vllm_path:
        print()
        vllm_path = find_dir_by_pattern("vllm-")
    assert vllm_path
    return [vllm_path, vllm_path / "requirements"]
