import bm25s
from tqdm import tqdm
from .models import MinimalSource
from .cli_commands.cli_models import (
    IndexArgs, SearchArgs, SearchDatasetArgs, AnswerArgs,
    AnswerDatasetArgs, EvaluateArgs)
from .cli_commands import Index


class StudentCLI:
    def index(self, *,  max_chunk_size: int = 2000):
        Index(max_chunk_size)

    def search(self, query: str, k: int = 5):
        #args = SearchArgs(query=query, k=k)
        #path = get_pattern_path("data/processed", "bm25")
        #retriver = bm25s.BM25().load(str(path))
        #results, scores = retriver.retrieve(**args.get_params())
        #print(results[0])
        #print(scores[0])
        pass

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
