import bm25s
from typing import Any
from pydantic import (BaseModel, Field, StrictInt, ConfigDict,
                      ValidationError, model_validator, field_validator)


class IndexArgs(BaseModel):
    max_chunk_size: StrictInt = Field(default=2000, ge=500)

    @field_validator("max_chunk_size")
    @classmethod
    def _hard_cap(cls, value: int) -> int:
        return value if value <= 2000 else 2000

    def get_params(self) -> dict[str, int]:
        return {"max_chunk_size": self.max_chunk_size}


class SearchArgs(BaseModel):
    query: str = Field(min_length=1)
    k: StrictInt = Field(default=5, ge=1)

    def get_params(self) -> dict[str, Any]:
        return {"query_tokens": bm25s.tokenize(self.query),
                "k": self.k}


class SearchDatasetArgs(BaseModel):
    model_config = ConfigDict(strict=True)

    dataset_path: str = Field(min_length=7)
    k: int = Field(default=5, ge=1, le=100)
    save_directory: str

    @model_validator(mode="after")
    def final_validate(self):
        if not self.dataset_path.endswith(".json"):
            raise ValidationError("Invalid dataset_path")
        try:
            with open(self.dataset_path):
                pass
        except FileNotFoundError:
            raise ValidationError("File not exist")
        return self


class AnswerArgs(BaseModel):
    question: str = Field(strict=True)
    k: int = Field(default=5, ge=1, le=100, strict=True)


class AnswerDatasetArgs(BaseModel):
    model_config = ConfigDict(strict=True)

    student_search_results_path: str = Field(min_length=7)
    save_directory: str

    @model_validator(mode="after")
    def final_validate(self):
        if not self.student_search_results_path.endswith(".json"):
            raise ValidationError("Invalid dataset_path")
        try:
            with open(self.student_search_results_path):
                pass
        except FileNotFoundError:
            raise ValidationError("File not exist")
        return self


class EvaluateArgs(BaseModel):
    ...
