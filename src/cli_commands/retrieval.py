import uuid
import bm25s
from tqdm import tqdm
from pathlib import Path
from src.errors import RetrivalError
from src.consts import INDEX_PATH
from src.models import (
    MinimalSource, StudentSearchResults,
    MinimalSearchResults, RagDataset
    )


def search_query(query: str, k: int, index_path: str,
                 loaded_chunks: list[MinimalSource],
                 question_id: str = str(uuid.uuid4())) -> MinimalSearchResults:
    index = Path(index_path)
    if not (index.exists() or index.is_dir()):
        raise RetrivalError("Index not found. Run 'index' first.")
    retriever = bm25s.BM25.load(index)
    tokenized_query = bm25s.tokenize(query)
    retrieved_sources = retriever.retrieve(tokenized_query, k=k)
    search_results_index = []
    for i, s in enumerate(retrieved_sources.scores[0]):
        if not s == 0:
            search_results_index.append(
                retrieved_sources.documents[0][i]
                )
    search_results: list[MinimalSource] = []
    for i in search_results_index:
        search_results.append(loaded_chunks[i])
    return MinimalSearchResults(
        question_id=question_id,
        question=query,
        retrieved_sources=search_results
        )


def search_query_dataset(ragdatase: RagDataset, k: int,
                         loaded_chunks: list[MinimalSource]
                         ) -> StudentSearchResults:
    questions_results = [
        search_query(question.question, k, INDEX_PATH,
                     loaded_chunks, question.question_id)
        for question in tqdm(ragdatase.rag_questions,
                             desc="Searching dataset")
        ]
    return StudentSearchResults(search_results=questions_results, k=k)
