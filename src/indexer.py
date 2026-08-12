import ast
import os
import re
from pathlib import Path


def get_vllm_path() -> Path:
    vllm_path_list = ["" + dir_name
                      for dir_name in os.listdir()
                      if re.fullmatch("^vllm.*", dir_name)]
    vllm_path = ""
    if vllm_path_list:
        vllm_path = vllm_path_list[0]
    if not vllm_path:
        raise FileNotFoundError("vllm not found")
    path = Path(vllm_path)
    if not path.is_dir():
        raise FileNotFoundError("vllm is not directory")
    return path


def get_all_files(path: Path, pattern: str):
    python_file_list: list[Path] = []
    for p in path.iterdir():
        if p.is_file() and p.suffix == pattern:
            python_file_list.append(p)
        if p.is_dir():
            python_file_list += get_all_files(p, pattern)
    return python_file_list
