from .models import MinimalSource
from .cli_models import (IndexArgs, SearchArgs, SearchDatasetArgs, AnswerArgs,
                         AnswerDatasetArgs, EvaluateArgs)
from .indexer import (get_vllm_path, get_all_files, chunk_md_file,
                      chunk_python_file, dump_chunks, index_chunks)


class StudentCLI:
    def index(self, *,  max_chunk_size: int = 1000):
        IndexArgs(max_chunk_size=max_chunk_size)
        vllm_path = get_vllm_path()
        py_files = get_all_files(vllm_path, ".py")
        md_files = get_all_files(vllm_path, ".md")
        md_chunks: list[MinimalSource] = []
        py_chunks: list[MinimalSource] = []
        for file in py_files:
            py_chunks += chunk_python_file(file, max_chunk_size)
        for file in md_files:
            md_chunks += chunk_md_file(file, max_chunk_size)
        dump_chunks(py_chunks, md_chunks)
        index_chunks(py_chunks, md_chunks)

    def search(self, *args, **kargs):
        cargs = SearchArgs()
        assert cargs
        print("Search", args, kargs)

    def search_dataset(self, *, dataset_path: str,
                       save_directory: str, k: int = 5):
        args = SearchDatasetArgs(dataset_path=dataset_path,
                                 k=k,
                                 save_directory=save_directory)
        print("Search_dataset", args)

    def answer(self, question: str, *, k: int = 5):
        args = AnswerArgs(question=question, k=k)
        print("Answer", args)

    def answer_dataset(self, student_search_results_path: str = "",
                       save_directory: str = ""):
        args = AnswerDatasetArgs(
            student_search_results_path=student_search_results_path,
            save_directory=save_directory
                                 )
        print("Answer_dataser", args)

    def evaluate(self):
        args = EvaluateArgs()
        print("Evaluate", args)
