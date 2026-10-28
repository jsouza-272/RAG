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
            print(question_id, r.question_id, question_id==r.question_id, i)
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
        AssertionError: If the question is not an instance of AnsweredQuestion.
        AssertionError: If the question index is not found in the student dataset.
    """

    assert dataset.rag_questions
    assert student_dataset.search_results
    question = dataset.rag_questions.pop()
    question_id = question.question_id
    question_index = search_question(question_id, student_dataset)
    assert question_index >= 0
    assert isinstance(question, AnsweredQuestion)
    return (
        question,
        student_dataset.search_results[question_index]
        )


def validade_chunk(src: MinimalSource, student: MinimalSource) -> bool:
    """Validates whether a student's source chunk is a valid portion of the
    original source chunk.

    Args:
        src (MinimalSource): The original source chunk to validate against.
        student (MinimalSource): The student's source chunk to be validated.

    Returns:
        bool: True if the student's chunk is a valid portion of the
        original source chunk, False otherwise.
        A valid portion is defined as having at least 5% overlap
        with the union of the two chunks.
    """

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


def question_recall(src: list[MinimalSource],
                    student: list[MinimalSource]) -> float:
    """Calculates the recall score based on the comparison
    of source materials between a reference list and a student's list.

    Args:
        src (list[MinimalSource]): A list of reference sources to be recalled.
        student (list[MinimalSource]): A list of sources provided by
        the student.

    Returns:
        float: The recall score, which is the ratio of correctly recalled
        sources to the total number of reference sources.
    """

    score = 0
    for source in src:
        for student_source in student:
            if validade_chunk(source, student_source):
                score += 1
                break
    return score / len(src)


def recall(dataset: RagDataset,
           student: StudentSearchResults,
           k: int = 5) -> float:
    score_sum = 0
    dataset_size = len(dataset.rag_questions)
    if student.k < k:
        raise EvaluateError(
            f"Student results were searched with k={student.k}, "
            f"but recall@{k} "
            f"was requested. Re-run search_dataset with --k >= {k}."
        )
    #try:
    #    for dataset_sources, student_sources in get_next_question(dataset,
    #                                                              student):
    #        score_sum += question_recall(
    #            dataset_sources.sources,
    #            student_sources.retrieved_sources[:k]
    #            )
    #        print("sss", score_sum)
    #except AssertionError:
    #    pass
    for i in range(dataset_size):
        dataset_sources, student_sources = get_next_question(dataset,
                                                             student)
        score_sum += question_recall(
            dataset_sources.sources,
            student_sources.retrieved_sources[:k]
            )
        print("sss", score_sum)
    return score_sum / dataset_size
