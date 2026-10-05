import json
import bm25s
from pathlib import Path
from src.models import RagDataset
from ..consts import (
    INDEX_PATH
)


class Search():
    def __init__(self, query: str, k: int = 5) -> None:
        args = SearchArgs(query=query, k=k)
        if not Path(INDEX_PATH).exists():
            raise FileNotFoundError("data not exists")
        retriever = bm25s.BM25().load(INDEX_PATH,
                                      load_corpus=True)
        retrieved_sources = retriever.retrieve(bm25s.tokenize(args.query),
                                               k=args.k)
        print(retrieved_sources.scores)
        print(retrieved_sources.documents)

