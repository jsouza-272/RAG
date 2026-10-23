from tqdm import tqdm
from typing import Any
from pathlib import Path
from .llm_wrapper import LLMWrapper
from .cli_commands import (
    index_and_save_chunks, chunk_md_file, chunk_python_file,
    parse_student_search_results_path, parse_save_directory,
    parse_query, parse_max_chunk_size, parse_k, parse_dataset_path,
    search_query, search_query_dataset
    )
from .file_io import (
    find_dir_by_pattern, find_files_by_suffix, dump_chunks,
    load_chunk, load_dataset, dump_search_results, valid_txt_parents,
    load_student_search_results, dump_student_answers
)
from .models import (
    MinimalSource, MinimalAnswer, StudentSearchResultsAndAnswer
    )
from .consts import (
    CHUNKS_PATH, INDEX_PATH
)


class StudentCLI:
    def index(self, *args: Any, max_chunk_size: int = 2000) -> None:
        if args:
            raise KeyError(f"ERROR: too many arguments {args}")
        max_chunk_size = parse_max_chunk_size(max_chunk_size)
        vllm_path = find_dir_by_pattern("vllm-")
        md_files = find_files_by_suffix(vllm_path, ".md")
        py_files = find_files_by_suffix(vllm_path, ".py")
        txt_files = [
            fpath
            for fpath in find_files_by_suffix(vllm_path, ".txt")
            if fpath.parent in valid_txt_parents(vllm_path)
        ]
        chunks: list[MinimalSource] = []
        for file in tqdm(md_files + py_files + txt_files, "Chunking files",
                         leave=False):
            if file.suffix == ".py":
                chunks += chunk_python_file(file, max_chunk_size)
            else:
                chunks += chunk_md_file(file, max_chunk_size)
        dump_chunks(chunks, CHUNKS_PATH)
        index_and_save_chunks(chunks)

    def search(self, query: str, *args: Any, k: int = 5) -> None:
        if args:
            raise KeyError(f"ERROR: too many arguments {args}")
        query = parse_query(query)
        k = parse_k(k)
        loaded_chunks = load_chunk(Path(CHUNKS_PATH))
        results = search_query(query, k, INDEX_PATH, loaded_chunks)
        print(results)

    def search_dataset(self, *args: Any, dataset_path: str,
                       save_directory: str, k: int = 5) -> None:
        if args:
            raise KeyError(f"ERROR: too many arguments {args}")
        dataset = parse_dataset_path(dataset_path)
        save_directory_path = parse_save_directory(save_directory)
        k = parse_k(k)
        ragdataset = load_dataset(dataset)
        loaded_chunks = load_chunk(Path(CHUNKS_PATH))
        results = search_query_dataset(ragdataset, k, loaded_chunks)
        dump_search_results(results, save_directory_path, dataset)

    def answer(self, query: str, *args: Any, k: int = 5) -> None:
        if args:
            raise KeyError(f"ERROR: too many arguments {args}")
        query = parse_query(query)
        k = parse_k(k)
        loaded_chunks = load_chunk(Path(CHUNKS_PATH))
        results = search_query(query, k, INDEX_PATH, loaded_chunks)
        answer = LLMWrapper().generation_pipeline(
            results.retrieved_sources, query
            )
        print(MinimalAnswer(
            question=query,
            retrieved_sources=results.retrieved_sources,
            answer=answer
        ))

    def answer_dataset(self, *args: Any, student_search_results_path: str,
                       save_directory: str) -> None:
        if args:
            raise KeyError(f"ERROR: too many arguments {args}")
        student_search_results = parse_student_search_results_path(
            student_search_results_path)
        save_directory_path = parse_save_directory(save_directory)

        dataset = load_student_search_results(student_search_results)
        llm = LLMWrapper()
        answer_results = []
        for item in dataset.search_results:
            answer = llm.generation_pipeline(
                item.retrieved_sources,
                item.question
            )
            answer_results.append(MinimalAnswer(
                question_id=item.question_id,
                question=item.question,
                retrieved_sources=item.retrieved_sources,
                answer=answer
            ))
        dump_student_answers(
            StudentSearchResultsAndAnswer(
                search_results=answer_results,
                k=dataset.k
                ),
            save_dir=save_directory_path,
            dataset=student_search_results
        )

    def evaluate(self) -> None:
        ...
