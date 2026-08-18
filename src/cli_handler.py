import bm25s
from tqdm import tqdm
from .models import MinimalSource
from .cli_models import (IndexArgs, SearchArgs, SearchDatasetArgs, AnswerArgs,
                         AnswerDatasetArgs, EvaluateArgs)
from .indexer import (get_pattern_path, get_all_files, chunk_md_file,
                      chunk_python_file, dump_chunks, index_chunks)


class StudentCLI:
    def index(self, *,  max_chunk_size: int = 2000):
        args = IndexArgs(max_chunk_size=max_chunk_size)
        vllm_path = get_pattern_path("data/raw")
        py_files = get_all_files(vllm_path, ".py")
        md_files = get_all_files(vllm_path, ".md")
        md_chunks: list[MinimalSource] = []
        py_chunks: list[MinimalSource] = []
        for file in tqdm(py_files + md_files,
                         "Chunking files", leave=False):
            if file.suffix == ".py":
                py_chunks += chunk_python_file(file, **args.get_params())
            else:
                md_chunks += chunk_md_file(file, **args.get_params())

        dump_chunks(py_chunks, md_chunks)
        index_chunks(py_chunks, md_chunks)

    def search(self, query: str, k: int = 5):
        args = SearchArgs(query=query, k=k)
        path = get_pattern_path("data/processed", "bm25")
        retriver = bm25s.BM25().load(str(path), load_corpus=True)
        results, scores = retriver.retrieve(**args.get_params())
        print(results[0])
        print(scores[0])

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
