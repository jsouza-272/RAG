from src.errors import EvaluateError
from src.models import (
    RagDataset, StudentSearchResults,
    MinimalSource, AnsweredQuestion, MinimalSearchResults
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
    Validate the given RagDataset for integrity and correctness.

    This function checks the RagDataset for the following conditions:
    1. The dataset must not be empty.
    2. Each question must have a unique question ID.
    3. Each entry in the dataset must be an instance of AnsweredQuestion.
    4. Each question must have associated sources.

    Args:
        dataset (RagDataset): The dataset to validate.

    Raises:
        EvaluateError: If the dataset is empty, contains duplicate question
        IDs, contains invalid entries, or has questions without sources.
    """

    id_list = []
    if not dataset.rag_questions:
        raise EvaluateError("Empty dataset")
    for d in dataset.rag_questions:
        if d.question_id in id_list:
            raise EvaluateError("Duplicate question")
        if not isinstance(d, AnsweredQuestion):
            raise EvaluateError("Invalid dataset")
        if not d.sources:
            raise EvaluateError("Invalid dataset")
        id_list.append(id)


def get_next_question(dataset: RagDataset,
                      student_dataset: StudentSearchResults,
                      index: int
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
        AssertionError: If the question index is not found in the student
        dataset.
    """

    assert dataset.rag_questions
    assert student_dataset.search_results
    question = dataset.rag_questions[index]
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
    """
    Calculates the recall score for a given dataset and student search results.

    This function computes the recall by comparing the sources retrieved by a
    student  against the sources available in the dataset for a specified
    number of top results (k). It raises an error if the number of results
    retrieved by the student is less than k.

    Args:
        dataset (RagDataset): The dataset containing the questions and their
                              sources.
        student (StudentSearchResults): The search results of the student
                                        containing retrieved sources.
        k (int, optional): The number of top results to consider for recall
                           calculation. Defaults to 5.

    Returns:
        float: The average recall score across all questions in the dataset.

    Raises:
        EvaluateError: If the number of results retrieved by the student
        (student.k) is less than k.
    """

    validate_dataset(dataset)
    score_sum = 0
    dataset_size = len(dataset.rag_questions)
    if student.k < k:
        raise EvaluateError(
            f"Student results were searched with k={student.k}, "
            f"but recall@{k} "
            f"was requested. Re-run search_dataset with --k >= {k}."
        )
    try:
        for i in range(dataset_size):
            dataset_sources, student_sources = get_next_question(
                dataset,
                student,
                i
                )
            score_sum += question_recall(
                dataset_sources.sources,
                student_sources.retrieved_sources[:k]
                )
    except AssertionError:
        pass
    return score_sum / dataset_size
