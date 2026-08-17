from .cli_models import IndexArgs, SearchArgs, SearchDatasetArgs, AnswerArgs
from .cli_models import AnswerDatasetArgs, EvaluateArgs


class StudentCLI:
    def index(self, *,  max_chunk_size: int = 1000):
        args = IndexArgs(max_chunk_size=max_chunk_size)
        print("Index", args)

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
