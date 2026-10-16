import json
from pydantic import ValidationError
from pathlib import Path
from src.errors import LoadError
from src.models import MinimalSource, RagDataset


def load_chunk(chunk_file: Path) -> list[MinimalSource]:
    if not chunk_file.exists():
        raise LoadError("Chunk file not found, run 'index' first")
    try:
        with open(chunk_file) as file:
            chunk_json = json.load(file)
        chunks = [MinimalSource(**chunk) for chunk in chunk_json]
    except (json.JSONDecodeError, ValidationError):
        raise LoadError("Invalid json format")
    return chunks


def load_dataset(dataset_path: Path) -> RagDataset:
    try:
        with open(dataset_path) as file:
            return RagDataset(**json.load(file))
    except (ValidationError, json.JSONDecodeError):
        raise LoadError("Invalid json format")
