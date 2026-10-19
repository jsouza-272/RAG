from tqdm import tqdm
from pathlib import Path
from src.errors import (
    ScanError, InvalidFileTypeError
    )
from src.consts import INVALID_PATHS


def find_files_by_suffix(dir: Path, suffix: str,
                         pbar: tqdm | None = None) -> list[Path]:
    file_list: list[Path] = []
    if isinstance(pbar, tqdm):
        pbar.update(1)
    for p in dir.iterdir():
        if p.is_file() and p.suffix == suffix:
            file_list.append(p)
        if p.is_dir():
            file_list += find_files_by_suffix(p, suffix)
    return file_list


def is_valid_dir(dir: Path) -> bool:
    return dir.parts[0] not in INVALID_PATHS and dir.is_dir()


def find_dir_by_pattern(pattern: str, base_dir_path: str = ".") -> Path:
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
