from .cli_commands.cli_models import (
    AnswerArgs,
    AnswerDatasetArgs, EvaluateArgs)
from .cli_commands import Index, Search, SearchDataset


class StudentCLI:
    def index(self, *args,  max_chunk_size: int = 2000):
        if args:
            raise ValueError("akjdas")
        Index(max_chunk_size)

    def search(self, query: str, *, k: int = 5):
        Search(query, k)

    def search_dataset(self, *, dataset_path: str,
                       save_directory: str, k: int = 5):
        SearchDataset(dataset_path, save_directory, k)

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
