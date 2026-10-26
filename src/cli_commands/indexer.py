import re
import ast
import math
import bm25s
from tqdm import tqdm
from pathlib import Path
from src.models import MinimalSource


def index_and_save_chunks(chunks: list[MinimalSource]) -> None:
    """
    Index and save chunks of text for BM25 retrieval.

    This function takes a list of `MinimalSource` objects, extracts their
    content, tokenizes it, and indexes it using the BM25 algorithm.
    The indexed data is then saved to a specified file path.

    Args:
        chunks (list[MinimalSource]): A list of `MinimalSource` objects
        containing the text chunks to be indexed.

    Returns:
        None: This function does not return any value.

    Raises:
        Any exceptions raised during the indexing or saving process will
        propagate up to the caller.
    """

    corpus = [
        _.content
        for _ in tqdm(chunks, "Indexing", leave=False)
        ]
    tokeninzed_chunks = bm25s.tokenize(corpus)
    bm = bm25s.BM25()
    bm.index(tokeninzed_chunks)
    bm.save("data/processed/bm25_index")


def build_index_by_line(source: str) -> list[int]:
    """
    Builds an index of line start offsets from the given source string.

    Args:
        source (str): The input string from which to build the index.
        It can contain multiple lines.

    Returns:
        list[int]: A list of integers representing the starting offsets of
        each line in the source string.
    """

    line_start_offsets = [0]
    for line in source.splitlines(keepends=True):
        line_start_offsets.append(line_start_offsets[-1] + len(line))
    return line_start_offsets


def split_chunk(max_chunk_size: int, overlap_size: int,
                current_start: int, current_end: int,
                source: str, path: Path) -> list[MinimalSource]:
    """
    Splits a source string into chunks of a specified maximum size with
    a defined overlap.

    Args:
        max_chunk_size (int): The maximum size of each chunk.
        overlap_size (int): The size of the overlap between consecutive chunks.
        current_start (int): The starting index for the current chunk.
        current_end (int): The ending index for the current chunk.
        source (str): The source string to be split into chunks.
        path (Path): The file path associated with the source string.

    Returns:
        list[MinimalSource]: A list of MinimalSource objects representing
        the split chunks.
    """

    step = max_chunk_size - overlap_size
    min_chunks = math.ceil((current_end - current_start) / step)
    chunks: list[MinimalSource] = []
    for i in range(min_chunks):
        chunk_end = min(current_start + max_chunk_size, current_end)
        chunks.append(
            MinimalSource(file_path=path.as_posix(),
                          first_character_index=current_start,
                          last_character_index=chunk_end,
                          content=source[current_start:chunk_end]))
        current_start += step
    return chunks


def chunk_python_file(file_path: Path,
                      max_chunk_size: int) -> list[MinimalSource]:
    """
    Chunks a Python file into smaller segments based on specified
    maximum chunk size.

    This function reads a Python file, parses its Abstract Syntax Tree (AST),
    and divides the code into chunks. Each chunk is either a class definition,
    a function definition, or a generic block of code. The chunks are created
    such that their sizes do not exceed the specified maximum chunk size.

    Args:
        file_path (Path): The path to the Python file to be chunked.
        max_chunk_size (int): The maximum size of each chunk in characters.

    Returns:
        list[MinimalSource]: A list of `MinimalSource` objects representing
        the code chunks, each containing the file path, the starting and
        ending character indices, and the content of the chunk.
    """

    chunks_list: list[MinimalSource] = []
    code = ""
    with open(file_path) as file:
        code = file.read()
    start_offsets = build_index_by_line(code)
    ast_file = ast.parse(code)
    generic = False
    start_index = 0
    end_index = 0
    i = 0
    while i < len(ast_file.body):
        if isinstance(ast_file.body[i], ast.ClassDef):
            generic = False
            start_index = start_offsets[ast_file.body[i].lineno - 1]
            node = ast_file.body[i]
            assert node.end_lineno and node.end_col_offset
            end_index = start_offsets[node.end_lineno - 1
                                      ] + node.end_col_offset
        elif isinstance(ast_file.body[i],
                        (ast.FunctionDef, ast.AsyncFunctionDef)):
            generic = False
            start_index = start_offsets[ast_file.body[i].lineno - 1]
            node = ast_file.body[i]
            assert node.end_lineno and node.end_col_offset
            end_index = start_offsets[node.end_lineno - 1
                                      ] + node.end_col_offset
        else:
            start_index = start_offsets[ast_file.body[i].lineno - 1]
            generic = True
            while (i < len(ast_file.body)
                    and not isinstance(
                    ast_file.body[i],
                    (ast.FunctionDef,
                        ast.AsyncFunctionDef, ast.ClassDef))):
                node = ast_file.body[i]
                assert node.end_lineno and node.end_col_offset
                end_index = start_offsets[node.end_lineno - 1
                                          ] + node.end_col_offset
                i += 1
        if end_index - start_index > max_chunk_size:
            chunks_list.extend(split_chunk(
                max_chunk_size, int(max_chunk_size * 0.2),
                start_index, end_index, code, file_path))
        else:
            chunks_list.append(
                MinimalSource(file_path=file_path.as_posix(),
                              first_character_index=start_index,
                              last_character_index=end_index,
                              content=code[start_index:end_index]))
        if not generic:
            i += 1
    return chunks_list


def chunk_md_file(file_path: Path,
                  max_chunk_size: int) -> list[MinimalSource]:
    """
    Chunks a Markdown file into smaller segments based on a specified
    maximum chunk size.

    Args:
        file_path (Path): The path to the Markdown file to be chunked.
        max_chunk_size (int): The maximum size of each chunk in characters.

    Returns:
        list[MinimalSource]: A list of MinimalSource objects representing the
        chunks of the Markdown file.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        ValueError: If max_chunk_size is less than or equal to zero.

    Notes:
        The function reads the entire content of the Markdown file, identifies
        sections based on headers and code fences,
        and splits the content into chunks that do not exceed the specified
        maximum size.
    """

    chunks_list: list[MinimalSource] = []
    doc = ""
    with open(file_path) as file:
        doc = file.read()
    start_offsets = build_index_by_line(doc)
    doc_lines = doc.splitlines(keepends=True)
    loop = False
    in_fence = False
    start_index = 0
    end_index = 0
    i = 0
    while i < len(doc_lines):
        start_index = start_offsets[i]
        i += 1

        while (i < len(doc_lines)
                and (in_fence or not re.match(
                    r"^#{1,6}\s.*$", doc_lines[i]
                    ))):
            if re.match(r"^```", doc_lines[i]):
                in_fence = not in_fence
            end_index = start_offsets[i] + len(doc_lines[i])
            i += 1
            loop = True

        if end_index == start_index:
            i += 1
            continue

        if end_index - start_index > max_chunk_size:
            chunks_list.extend(split_chunk(
                max_chunk_size, int(max_chunk_size * 0.2),
                start_index, end_index, doc, file_path))
        else:
            chunks_list.append(
                MinimalSource(file_path=file_path.as_posix(),
                              first_character_index=start_index,
                              last_character_index=end_index,
                              content=doc[start_index:end_index]))

        if not loop:
            i += 1
        loop = False

    return chunks_list
