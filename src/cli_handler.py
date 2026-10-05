from .cli_commands.cli_models import (
    AnswerArgs,
    AnswerDatasetArgs, EvaluateArgs)


class StudentCLI:
    def index(self, *args,  max_chunk_size: int = 2000):
        if args:
            raise ValueError("akjdas")

    def search(self, query: str, *, k: int = 5):
        ...

    def search_dataset(self, *, dataset_path: str,
                       save_directory: str, k: int = 5):
        ...

    def answer(self, query: str, *, k: int = 5):
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
