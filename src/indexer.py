import ast
import os
import re
import json
from .models import MinimalSource
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


def dump_chunks(py_chunks: list[MinimalSource],
                md_chunks: list[MinimalSource]):
    path = Path("data/processed/chunks/chunks.json")
    path.parent.mkdir(mode=0o775, parents=True, exist_ok=True)
    path.touch(exist_ok=True)
    with open(path, mode="w") as file:
        json.dump([c.dump() for c in py_chunks + md_chunks], file)


def chunk_python_file(file_path: str) -> None:
    code = ""
    with open(file_path) as file:
        code = file.read()
    ast_file = ast.parse(code)
    chunk = ""
    for line in ast_file:
        if isinstance(line, ast.ClassDef):
            chunk = ast.get_source_segment(code, line)
        elif isinstance(line, (ast.FunctionDef, ast.AsyncFunctionDef)):
            chunk = ast.get_source_segment(code, line)
        else:
            # fazer flag para guardar o comeco desse bloco generico
            pass
        chunk
        # remover linha acima
