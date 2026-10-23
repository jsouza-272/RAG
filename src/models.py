import uuid
from typing import List
from pydantic import BaseModel, Field


class MinimalSource(BaseModel):
    """
    MinimalSource is a model that represents a source of content with
    associated metadata.

    Attributes:
        content (str): The content of the source.
        file_path (str): The path to the file containing the content.
        first_character_index (int): The index of the first character in the
        content.
        last_character_index (int): The index of the last character in the
        content.

    Methods:
        __str__() -> str: Returns a string representation of the MinimalSource
        instance.
        __repr__() -> str: Returns a detailed string representation of the
        MinimalSource instance for debugging.
    """

    content: str
    file_path: str
    first_character_index: int
    last_character_index: int

    def __str__(self) -> str:
        """
        Returns a string representation of the object.

        This method provides a formatted string that includes the file path,
        the index of the first character, and the index of the last character.

        Returns:
            str: A formatted string containing the file path, first character
            index, and last character index.
        """

        return (f"\nfile_path: {self.file_path!r}\n"
                f"first_character_index: {self.first_character_index}\n"
                f"last_character_index: {self.last_character_index}\n")

    def __repr__(self) -> str:
        """
        Returns a string representation of the object.

        This method provides a formatted string that includes the file path,
        the index of the first character, and the index of the last character.

        Returns:
            str: A formatted string containing the file path, first character
            index, and last character index.
        """

        return (f"\nfile_path: {self.file_path!r}\n"
                f"first_character_index: {self.first_character_index}\n"
                f"last_character_index: {self.last_character_index}\n")


class MinimalSearchResults(BaseModel):
    """
    MinimalSearchResults is a model that represents the results of a
    minimal search query.

    Attributes:
        question_id (str): A unique identifier for the question,
        generated as a UUID.
        question (str): The text of the question being searched.
        retrieved_sources (List[MinimalSource]): A list of sources that were
        retrieved in response to the question.

    Methods:
        __str__() -> str: Returns a string representation of the
        MinimalSearchResults instance.
        __repr__() -> str: Returns a detailed string representation of the
        MinimalSearchResults instance for debugging.
    """

    question_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    question: str
    retrieved_sources: List[MinimalSource]

    def __str__(self) -> str:
        """
        Returns a string representation of the object.

        The string includes the question ID, the question text,
        and the retrieved sources.

        Returns:
            str: A formatted string containing the question ID,
            question, and retrieved sources.
        """

        return (f"question_id: {self.question_id}\n"
                f"question: {self.question}\n"
                f"retrieved_sources: {self.retrieved_sources}")

    def __repr__(self) -> str:
        """
        Returns a string representation of the object.

        This method provides a formatted string that includes the question ID,
        the question text, and the retrieved sources.

        Returns:
            str: A formatted string containing the question ID, question,
            and retrieved sources.
        """

        return (f"\nquestion_id: {self.question_id}\n"
                f"question: {self.question}\n"
                f"retrieved_sources: {self.retrieved_sources}")


class MinimalAnswer(MinimalSearchResults):
    """
    MinimalAnswer is a class that represents a minimal answer to a search
    query, inheriting from MinimalSearchResults.

    Attributes:
        answer (str): The answer to the question.

    Methods:
        __str__() -> str:
            Returns a string representation of the MinimalAnswer instance,
            including question ID, question, answer, and retrieved sources.

        __repr__() -> str:
            Returns a detailed string representation of the MinimalAnswer
            instance, suitable for debugging.
    """

    answer: str

    def __str__(self) -> str:
        """
        Returns a string representation of the object.

        This method formats the object's attributes into a readable string,
        including the question ID, question text, answer, and retrieved
        sources.

        Returns:
            str: A formatted string containing the question ID, question,
            answer, and retrieved sources.
        """

        return (f"question_id: {self.question_id}\n"
                f"question: {self.question}\n"
                f"answer: {self.answer}\n"
                f"retrieved_sources: {self.retrieved_sources}")

    def __repr__(self) -> str:
        """
        Returns a string representation of the object.

        This method provides a formatted string that includes the question ID,
        the question text, the answer, and the retrieved sources.

        Returns:
            str: A string representation of the object containing the question
            ID, question, answer, and retrieved sources.
        """

        return (f"question_id: {self.question_id}\n"
                f"question: {self.question}\n"
                f"answer: {self.answer}\n"
                f"retrieved_sources: {self.retrieved_sources}")


class StudentSearchResults(BaseModel):
    """
    Class representing the search results for students.

    Attributes:
        search_results (List[MinimalSearchResults]): A list of minimal search
        results for students.
        k (int): An integer representing a specific parameter related to the
        search results.

    Methods:
        __str__() -> str: Returns a string representation of the search
        results and the parameter k.
    """

    search_results: List[MinimalSearchResults]
    k: int

    def __str__(self) -> str:
        """
        Returns a string representation of the object.

        This method formats the object's attributes, specifically
        `search_results` and `k`, into a readable string.

        Returns:
            str: A string that includes the search results and the value of k.
        """

        return (f"search_results: {self.search_results}\n"
                f"k: {self.k}")


class StudentSearchResultsAndAnswer(BaseModel):
    """
    Class representing the search results and answer for a student.

    Attributes:
        search_results (List[MinimalAnswer]): A list of minimal answers
        obtained from the search.
        k (int): An integer representing a specific parameter related to the
        search results.

    Methods:
        __str__() -> str: Returns a string representation of the search
        results and the value of k.
    """

    search_results: List[MinimalAnswer]
    k: int

    def __str__(self) -> str:
        """
        Returns a string representation of the object.

        This method formats the object's attributes, specifically
        `search_results` and `k`, into a readable string.

        Returns:
            str: A string that includes the search results and the value of k.
        """

        return (f"search_results: {self.search_results}\n"
                f"k: {self.k}")


class UnansweredQuestion(BaseModel):
    """
    UnansweredQuestion represents a question that has not yet received
     an answer.

    Attributes:
        question_id (str): A unique identifier for the question, generated
        as a UUID.
        question (str): The text of the question.
    """

    question_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    question: str


class AnsweredQuestion(UnansweredQuestion):
    """
    Class representing a question that has been answered.

    Attributes:
        sources (List[MinimalSource]): A list of sources that provide "
        "information related to the answered question.
        answer (str): The answer to the question.
    """

    sources: List[MinimalSource]
    answer: str


class RagDataset(BaseModel):
    """
    RagDataset is a class that represents a dataset containing a list
    of questions,
    which can be either answered or unanswered.

    Attributes:
        rag_questions (List[AnsweredQuestion | UnansweredQuestion]):
        A list of questions
        that are either answered or unanswered.
    """

    rag_questions: List[AnsweredQuestion | UnansweredQuestion]
