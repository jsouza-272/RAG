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
    """
    A command-line interface for managing student-related operations,
    including indexing, searching, and answering queries based on various
    file types.

    Methods:
        index(max_chunk_size: int = 2000) -> None:
            Indexes markdown, Python, and text files, chunking them into
            manageable sizes and saving the results.

        search(query: str, k: int = 5) -> None:
            Searches for a query in the indexed chunks and prints the results.

        search_dataset(dataset_path: str, save_directory: str,
        k: int = 5) -> None:
            Searches a specified dataset and saves the results to a given
            directory.

        answer(query: str, k: int = 5) -> None:
            Generates an answer to a query using a language model and
            prints the result.

        answer_dataset(student_search_results_path: str,
        save_directory: str) -> None:
            Processes a dataset of student search results, generates answers,
            and saves them to a specified directory.

        evaluate() -> None:
            Evaluates the performance of the system
            (implementation not provided).
    """

    def index(self, *args: Any, max_chunk_size: int = 2000) -> None:
        """
        Index files and create chunks from markdown, Python, and text files.

        This method processes files found in a specified directory, chunks
        them into smaller pieces based on a maximum chunk size, and saves the
        resulting chunks for further indexing.

        Args:
            max_chunk_size (int, optional): The maximum size of each chunk.
            Defaults to 2000.

        Raises:
            KeyError: If any additional arguments are provided to the function.

        Returns:
            None
        """

        if args:
            raise KeyError(f"ERROR: too many arguments {args}")
        max_chunk_size = parse_max_chunk_size(max_chunk_size)
        vllm_path = find_dir_by_pattern("vllm-", base_dir_path="data/raw")
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
        """
        Search for relevant results based on the provided query.

        This method processes the input query,
        validates the number of arguments,
        loads necessary data chunks, and retrieves search results.
        It raises an error if too many arguments are provided.

        Args:
            query (str): The search query string.
            *args (Any): Additional arguments (not used).
            k (int, optional): The number of results to return. Defaults to 5.

        Raises:
            KeyError: If more than one additional argument is provided.

        Returns:
            None: This function prints the search results directly.
        """

        if args:
            raise KeyError(f"ERROR: too many arguments {args}")
        query = parse_query(query)
        k = parse_k(k)
        loaded_chunks = load_chunk(Path(CHUNKS_PATH))
        results = search_query(query, k, INDEX_PATH, loaded_chunks)
        print(results)

    def search_dataset(self, *args: Any, dataset_path: str,
                       save_directory: str, k: int = 5) -> None:
        """
        Searches a dataset and saves the results to a specified directory.

        Args:
            dataset_path (str): The path to the dataset to be searched.
            save_directory (str): The directory where the search results
            will be saved.
            k (int, optional): The number of results to return. Defaults to 5.
            *args (Any): Additional arguments. Raises a KeyError if provided.

        Raises:
            KeyError: If any additional arguments are passed to the function.

        Returns:
            None
        """

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
        """
        Answers a given query by retrieving relevant information and
        generating a response.

        Args:
            query (str): The query string to be processed.
            *args (Any): Additional arguments that are not used.
            Raises a KeyError if provided.
            k (int, optional): The number of results to retrieve.
            Defaults to 5.

        Raises:
            KeyError: If any additional arguments are provided beyond
            the expected ones.

        Returns:
            None: This function prints the answer to the console
            and does not return a value.
        """

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
        """
        Answers a dataset of student search results and saves the answers to a
        specified directory.

        This method processes the student search results, generates answers
        using a language model, and saves the results in a specified directory.
        It raises an error if any additional arguments are provided.

        Args:
            student_search_results_path (str): The path to the student search
            results to be processed.
            save_directory (str): The directory where the generated answers
            will be saved.

        Raises:
            KeyError: If any additional arguments are provided beyond the
            expected ones.

        Returns:
            None
        """

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
