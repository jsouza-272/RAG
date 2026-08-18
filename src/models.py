import uuid
from typing import List
from pydantic import BaseModel, Field


class MinimalSource(BaseModel):
    content: str
    file_path: str
    first_character_index: int
    last_character_index: int

    def dump(self) -> dict:
        return {"file_path": self.file_path,
                "content": self.content,
                "first_character_index": self.first_character_index,
                "last_character_index": self.last_character_index}

    def __repr__(self) -> str:
        return (f"file_path: {self.file_path}\n"
                f"first_character_index: {self.first_character_index}\n"
                f"last_character_index: {self.last_character_index}\n")


class UnansweredQuestion(BaseModel):
    question_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    question: str


class AnsweredQuestion(UnansweredQuestion):
    sources: List[MinimalSource]
    answer: str


class RagDataset(BaseModel):
    rag_questions: List[AnsweredQuestion | UnansweredQuestion]


class MinimalSearchResults(BaseModel):
    question_id: str
    question: str
    retrieved_sources: List[MinimalSource]


class MinimalAnswer(MinimalSearchResults):
    answer: str


class StudentSearchResults(BaseModel):
    search_results: List[MinimalSearchResults]
    k: int


class StudentSearchResultsAndAnswer(BaseModel):
    search_results: List[MinimalAnswer]
    k: int
