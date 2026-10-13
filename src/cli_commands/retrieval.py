import bm25s
from pathlib import Path
from src.models import MinimalSource
from src.errors import RetrivalError


def search_query(query: str, k: int, index_path: str,
                 loaded_chunks: list[MinimalSource]) -> list[MinimalSource]:
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
    return search_results
