import uuid
from typing import List
from pydantic import BaseModel, Field


class MinimalSource(BaseModel):
    content: str
    file_path: str
    first_character_index: int
    last_character_index: int

    def __str__(self) -> str:
        return (f"\nfile_path: {self.file_path!r}\n"
                f"first_character_index: {self.first_character_index}\n"
                f"last_character_index: {self.last_character_index}\n")

    def __repr__(self) -> str:
        return (f"\nfile_path: {self.file_path!r}\n"
                f"first_character_index: {self.first_character_index}\n"
                f"last_character_index: {self.last_character_index}\n")


class MinimalSearchResults(BaseModel):
    question_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    question: str
    retrieved_sources: List[MinimalSource]

    def __str__(self) -> str:
        return (f"question_id: {self.question_id}\n"
                f"question: {self.question}\n"
                f"retrieved_sources: {self.retrieved_sources}")

    def __repr__(self) -> str:
        return (f"\nquestion_id: {self.question_id}\n"
                f"question: {self.question}\n"
                f"retrieved_sources: {self.retrieved_sources}")


class MinimalAnswer(MinimalSearchResults):
    answer: str

    def __str__(self) -> str:
        return (f"question_id: {self.question_id}\n"
                f"question: {self.question}\n"
                f"answer: {self.answer}\n"
                f"retrieved_sources: {self.retrieved_sources}")

    def __repr__(self) -> str:
        return (f"question_id: {self.question_id}\n"
                f"question: {self.question}\n"
                f"answer: {self.answer}\n"
                f"retrieved_sources: {self.retrieved_sources}")


class StudentSearchResults(BaseModel):
    search_results: List[MinimalSearchResults]
    k: int

    def __str__(self) -> str:
        return (f"search_results: {self.search_results}\n"
                f"k: {self.k}")


class StudentSearchResultsAndAnswer(BaseModel):
    search_results: List[MinimalAnswer]
    k: int

    def __str__(self) -> str:
        return (f"search_results: {self.search_results}\n"
                f"k: {self.k}")


class UnansweredQuestion(BaseModel):
    question_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    question: str


class AnsweredQuestion(UnansweredQuestion):
    sources: List[MinimalSource]
    answer: str


class RagDataset(BaseModel):
    rag_questions: List[AnsweredQuestion | UnansweredQuestion]
