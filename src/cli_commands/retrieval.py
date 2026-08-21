import bm25s
from pathlib import Path
from .cli_models import SearchArgs


class Search():
    def __init__(self, query: str, k: int = 5) -> None:
        args = SearchArgs(query=query, k=k)
        if not Path("data/processed/bm25_index").exists():
            raise FileNotFoundError("data not exists")
        retriever = bm25s.BM25().load("data/processed/bm25_index",
                                      load_corpus=True)
        retrieved_sources = retriever.retrieve(bm25s.tokenize(args.query),
                                               k=args.k)
        print(retrieved_sources.scores)
        print(retrieved_sources.documents)
