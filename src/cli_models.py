from pydantic import BaseModel, Field, StrictInt, ConfigDict
from pydantic import ValidationError, model_validator


class IndexArgs(BaseModel):
    max_chunk_size: StrictInt = Field(default=2000, ge=500, le=5000)


class SearchArgs(BaseModel):
    ...


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
