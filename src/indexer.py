import ast
import os
import re
import json
import math
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
    '''if not path.is_dir():
        raise FileNotFoundError("vllm is not directory")
    if not path.is_dir():
        raise FileNotFoundError("vllm is not directory")
    if not path.is_dir():
        raise FileNotFoundError("vllm is not directory")
    if not path.is_dir():
        raise FileNotFoundError("vllm is not directory")
    if not path.is_dir():
        raise FileNotFoundError("vllm is not directory")
    if not path.is_dir():
        raise FileNotFoundError("vllm is not directory")
    if not path.is_dir():
        raise FileNotFoundError("vllm is not directory")
    if not path.is_dir():
        raise FileNotFoundError("vllm is not directory")
    if not path.is_dir():
        raise FileNotFoundError("vllm is not directory")
    if not path.is_dir():
        raise FileNotFoundError("vllm is not directory")
    if not path.is_dir():
        raise FileNotFoundError("vllm is not directory")
    if not path.is_dir():
        raise FileNotFoundError("vllm is not directory")
    if not path.is_dir():
        raise FileNotFoundError("vllm is not directory")
    if not path.is_dir():
        raise FileNotFoundError("vllm is not directory")
    if not path.is_dir():
        raise FileNotFoundError("vllm is not directory")
    if not path.is_dir():
        raise FileNotFoundError("vllm is not directory")
    if not path.is_dir():
        raise FileNotFoundError("vllm is not directory")
    if not path.is_dir():
        raise FileNotFoundError("vllm is not directory")
    if not path.is_dir():
        raise FileNotFoundError("vllm is not directory")
    if not path.is_dir():
        raise FileNotFoundError("vllm is not directory")
    if not path.is_dir():
        raise FileNotFoundError("vllm is not directory")
    if not path.is_dir():
        raise FileNotFoundError("vllm is not directory")
    if not path.is_dir():
        raise FileNotFoundError("vllm is not directory")
    if not path.is_dir():
        raise FileNotFoundError("vllm is not directory")
    if not path.is_dir():
        raise FileNotFoundError("vllm is not directory")'''
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


def build_index_by_line(source: str) -> list[int]:
    line_start_offsets = [0]
    for line in source.splitlines(keepends=True):
        line_start_offsets.append(line_start_offsets[-1] + len(line))
    return line_start_offsets


def chunk_python_file(file_path: str,
                      max_chunk_size: int) -> list[MinimalSource]:
    chunks_list: list[MinimalSource] = []
    current_chunks: list[MinimalSource] = []
    code = ""
    with open(file_path) as file:
        code = file.read()
    start_offsets = build_index_by_line(code)
    ast_file = ast.parse(code)
    generic = False
    start_index = 0
    end_index = 0
    for line in ast_file.body:
        current_chunks = []
        if isinstance(line, ast.ClassDef):
            generic = False
            start_index = start_offsets[line.lineno - 1]
            end_index = start_offsets[
                line.end_lineno - 1] + line.end_col_offset
        elif isinstance(line, (ast.FunctionDef, ast.AsyncFunctionDef)):
            generic = False
            start_index = start_offsets[line.lineno - 1]
            end_index = start_offsets[
                line.end_lineno - 1] + line.end_col_offset
        else:
            if not generic:
                start_index = start_offsets[line.lineno - 1]
            generic = True
            end_index = start_offsets[
                line.end_lineno - 1] + line.end_col_offset
        current_chunks.append({"first_character_index": start_index,
                               "last_character_index": end_index})
        if end_index - start_index > max_chunk_size:
            current_chunks = split_chunk(
                max_chunk_size, int(max_chunk_size * 0.1),
                start_index, end_index)
        chunks_list.extend(MinimalSource(file_path=file_path, **chunk)
                           for chunk in current_chunks)
        print("\n\033[38;2;200;0;200m", "="*100, "\033[0m\n")
        print(start_index, end_index)
        print("got:", code[start_index:end_index])
        print()
        print("expected:", ast.get_source_segment(code, line))
    print("\n\033[38;2;200;0;200m", "="*100, "\033[0m\n")
    return chunks_list


def split_chunk(max_chunk_size: int, overlap_size: int,
                current_start: int, current_end: int) -> dict:
    step = max_chunk_size - overlap_size
    min_chunks = math.ceil((current_end - current_start) / step)
    chunks: list[dict] = []
    for i in range(min_chunks):
        chunk_info = {"first_character_index": current_start,
                      "last_character_index": min(
                          current_start + max_chunk_size, current_end)}
        current_start += step
        chunks.append(chunk_info)
    return chunks
