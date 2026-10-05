class ParseError(Exception):
    def __init__(self, argument: str, msg: str) -> None:
        super().__init__(f"ParseError ({argument}): {msg}")


class TopKError(ParseError):
    def __init__(self, msg: str) -> None:
        super().__init__("top-k", msg)


class QueryError(ParseError):
    def __init__(self, msg: str) -> None:
        super().__init__("query", msg)


class QuestionError(ParseError):
    def __init__(self, msg: str) -> None:
        super().__init__("question", msg)


class MaxChunkSizeError(ParseError):
    def __init__(self, msg: str) -> None:
        super().__init__("max_chunk_size", msg)


class DataSetPathError(ParseError):
    def __init__(self, msg: str) -> None:
        super().__init__("dataset_path", msg)


class SaveDirectoryError(ParseError):
    def __init__(self, msg: str) -> None:
        super().__init__("save_directory", msg)


class StudentSearchResultsPathError(ParseError):
    def __init__(self, msg: str) -> None:
        super().__init__("student_search_results_path", msg)
