from tqdm import tqdm
from .cli_commands import (
    index_and_save_chunks, chunk_md_file, chunk_python_file,
    parse_student_search_results_path, parse_save_directory,
    parse_query, parse_max_chunk_size, parse_k, parse_dataset_path
    )
from .file_io import (
    find_dir_by_pattern, find_files_by_suffix, dump_chunks
)
from .models import MinimalSource
from .consts import (
    CHUNKS_PATH
)


class StudentCLI:
    def index(self, *,  max_chunk_size: int = 2000):
        max_chunk_size = parse_max_chunk_size(max_chunk_size)
        vllm_path = find_dir_by_pattern("vllm-")
        md_files = find_files_by_suffix(vllm_path, ".md")
        py_files = find_files_by_suffix(vllm_path, ".py")
        md_chunks: list[MinimalSource] = []
        py_chunks: list[MinimalSource] = []
        for file in tqdm(md_files + py_files, "Chunking files"):
            if file.suffix == ".py":
                py_chunks += chunk_python_file(file, max_chunk_size)
            else:
                md_chunks += chunk_md_file(file, max_chunk_size)
        dump_chunks(md_chunks + py_chunks, CHUNKS_PATH)
        index_and_save_chunks(py_chunks, md_chunks)

    def search(self, query: str, *, k: int = 5):
        query = parse_query(query)
        k = parse_k(k)

    def search_dataset(self, *, dataset_path: str,
                       save_directory: str, k: int = 5):
        dataset = parse_dataset_path(dataset_path)
        save_directory_path = parse_save_directory(save_directory)
        k = parse_k(k)
        print(dataset, save_directory_path)

    def answer(self, query: str, *, k: int = 5):
        query = parse_query(query)
        k = parse_k(k)
        print(query, k)

    def answer_dataset(self, student_search_results_path: str = "",
                       save_directory: str = ""):
        student_search_results = parse_student_search_results_path(
            student_search_results_path)
        save_directory_path = parse_save_directory(save_directory)
        print(student_search_results, save_directory_path)

    def evaluate(self):
        ...
