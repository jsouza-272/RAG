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


class MinimalSearchResults(BaseModel):
    question_id: str
    question: str
    retrieved_sources: List[MinimalSource]

    def dump(self) -> dict:
        return {
            "question_id": self.question_id,
            "question": self.question,
            "retrieved_sources": [
                min_source.dump() for min_source in self.retrieved_sources
                ]
            }

    def __repr__(self) -> str:
        return (f"question_id: {self.question_id}\n"
                f"question: {self.question}\n"
                f"retrieved_sources: {self.retrieved_sources}\n")


class StudentSearchResults(BaseModel):
    search_results: List[MinimalSearchResults]
    k: int

    def dump(self) -> dict:
        return {
            "search_results": [
                min_search.dump() for min_search in self.search_results
            ],
            "k": self.k
        }


class UnansweredQuestion(BaseModel):
    question_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    question: str


class AnsweredQuestion(UnansweredQuestion):
    sources: List[MinimalSource]
    answer: str


class MinimalAnswer(MinimalSearchResults):
    answer: str


class StudentSearchResultsAndAnswer(BaseModel):
    search_results: List[MinimalAnswer]
    k: int


class RagDataset(BaseModel):
    rag_questions: List[AnsweredQuestion | UnansweredQuestion]
