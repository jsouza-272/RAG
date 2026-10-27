from src.errors import EvaluateError
from src.models import (
    RagDataset, StudentSearchResults,
    MinimalSource, UnansweredQuestion,
    AnsweredQuestion, MinimalSearchResults
    )


def search_question(question_id: str,
                    student_dataset: StudentSearchResults) -> int:
    """
    Search for a question in the student dataset.

    Args:
        question_id (str): The ID of the question to search for.
        student_dataset (StudentSearchResults): The dataset containing
        student search results.

    Returns:
        int: The index of the question in the dataset if found, otherwise -1.
    """

    for i, r in enumerate(student_dataset.search_results):
        if question_id == r.question_id:
            return i
    return -1


def validate_dataset(dataset: RagDataset) -> None:
    """
    Validate the given dataset for unanswered questions.

    This function checks if the provided dataset contains any instances of
    `UnansweredQuestion`. If such instances are found, an `EvaluateError`
    is raised indicating that the dataset is invalid.

    Args:
        dataset (RagDataset): The dataset to be validated.

    Raises:
        EvaluateError: If the dataset contains any unanswered questions.
    """

    if any([
            isinstance(d, UnansweredQuestion)
            for d in dataset.rag_questions
            ]):
        raise EvaluateError("invalid dataset")


def get_next_question(dataset: RagDataset,
                      student_dataset: StudentSearchResults
                      ) -> tuple[AnsweredQuestion, MinimalSearchResults]:
    """
    Get the next question from the dataset and its corresponding
    from the student dataset.

    Args:
        dataset (RagDataset): The dataset containing RAG questions.
        student_dataset (StudentSearchResults): The dataset containing
        results for the student.

    Returns:
        tuple[list[MinimalSource], list[MinimalSource]]: A tuple
        two lists:
            - The sources associated with the next question.
            - The retrieved sources from the student's search
            corresponding to the question.

    Raises:
        AssertionError: If the dataset contains questions or the
        dataset contains search results.
        TypeError: If the question is not an instance of AnsweredQuestion.
        IndexError: If the question index is not found in the student dataset.
    """

    assert not dataset.rag_questions
    assert not student_dataset.search_results
    question = dataset.rag_questions.pop()
    question_id = question.question_id
    question_index = search_question(question_id, student_dataset)
    assert question_index < 0
    assert isinstance(question, AnsweredQuestion)
    return (
        question,
        student_dataset.search_results[question_index]
        )


def validade_chunk(src: MinimalSource, student: MinimalSource) -> bool:
    if not src.file_path == student.file_path:
        return False

    start_index = max(src.first_character_index, student.first_character_index)
    end_index = min(src.last_character_index, student.last_character_index)
    inter = end_index - start_index

    if inter < 0:
        return False
    src_len = src.last_character_index - src.first_character_index
    student_len = student.last_character_index - student.first_character_index
    union = src_len + student_len - inter
    return inter / union >= 0.05


def question_recall() -> float:
    ...


def recall(dataset_sources: AnsweredQuestion,
            student_sources: MinimalSearchResults) -> float:
    ...
