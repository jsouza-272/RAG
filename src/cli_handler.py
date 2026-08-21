from .cli_commands.cli_models import (
    SearchDatasetArgs, AnswerArgs,
    AnswerDatasetArgs, EvaluateArgs)
from .cli_commands import Index, Search


class StudentCLI:
    def index(self, *args,  max_chunk_size: int = 2000):
        if args:
            raise ValueError("akjdas")
        Index(max_chunk_size)

    def search(self, query: str, *args, k: int = 5):
        Search(query, k)

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
