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
    """
    Search for relevant sources based on a query using a BM25 retriever.

    Args:
        query (str): The search query string.
        k (int): The number of top results to retrieve.
        index_path (str): The file path to the index directory.
        loaded_chunks (list[MinimalSource]): A list of pre-loaded source
        chunks to search from.
        question_id (str, optional): A unique identifier for the question.
        Defaults to a new UUID.

    Returns:
        MinimalSearchResults: An object containing the question ID, the
        original query, and the retrieved sources.

    Raises:
        RetrievalError: If the index does not exist or is not a directory.
    """

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
    """
    Searches a dataset for relevant results based on provided queries.

    Args:
        ragdatase (RagDataset): The dataset containing the questions
        to be searched.
        k (int): The number of top results to return for each query.
        loaded_chunks (list[MinimalSource]): A list of pre-loaded data chunks
        to search through.

    Returns:
        StudentSearchResults: An object containing the search results for
        the queries, including the number of results requested (k).
    """

    questions_results = [
        search_query(question.question, k, INDEX_PATH,
                     loaded_chunks, question.question_id)
        for question in tqdm(ragdatase.rag_questions,
                             desc="Searching dataset")
        ]
    return StudentSearchResults(search_results=questions_results, k=k)
