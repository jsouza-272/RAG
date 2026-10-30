*This project has been created as part of the 42 curriculum by jsouza.*

# RAG against the machine

## Description

A Retrieval-Augmented Generation (RAG) system that answers questions about the vLLM codebase. It indexes the repository, retrieves the most relevant snippets for a question with BM25, and generates a grounded answer with `Qwen/Qwen3-0.6B`. Retrieval quality is measured with recall@k.

## Instructions

Requirements: Python 3.10+, [uv](https://docs.astral.sh/uv/). The vLLM repository must be placed under `data/raw/`.

```bash
make install        # uv sync
make run            # run the main script
make debug          # run under pdb
make lint           # flake8 + mypy
make clean          # remove caches
```

Commands are invoked as `uv run python -m src <command> [options]`:

| Command | Purpose |
|---|---|
| `index --max_chunk_size N` | Chunk `data/raw/` and build the index under `data/processed/` |
| `search <query> --k N` | Top-k sources for one query |
| `search_dataset --dataset_path P --k N --save_directory D` | Search a whole dataset (`StudentSearchResults` JSON) |
| `answer <query> --k N` | Answer one query from the retrieved context |
| `answer_dataset --student_search_results_path P --save_directory D` | Answers for a dataset (`StudentSearchResultsAndAnswer` JSON) |
| `evaluate --student_search_results_path P --dataset_path P` | Own recall@k against a ground-truth dataset |

All input and output paths are CLI arguments. The default `k` is 10.

## Example usage

```bash
uv run python -m src index --max_chunk_size 2000
uv run python -m src search_dataset \
  --dataset_path data/datasets/UnansweredQuestions/dataset_docs_public.json \
  --k 10 \
  --save_directory data/output/search_results/UnansweredQuestions
uv run python -m src evaluate \
  --student_search_results_path data/output/search_results/UnansweredQuestions/dataset_docs_public.json \
  --dataset_path data/datasets/AnsweredQuestions/dataset_docs_public.json
uv run python -m src answer_dataset \
  --student_search_results_path data/output/search_results/UnansweredQuestions/dataset_docs_public.json \
  --save_directory data/output/search_results_and_answer/UnansweredQuestions
```

## System architecture

1. **Indexing** (`index`): collect `.py` and `.md` files, chunk them, persist the chunks to JSON and build a BM25 index.
2. **Retrieval** (`search`, `search_dataset`): pure BM25 top-k. No LLM and no score filtering at this stage, to preserve recall.
3. **Augmenting** (`answer`, `answer_dataset`): the retrieved chunks (at most 5) are placed in the model context.
4. **Generation**: `Qwen/Qwen3-0.6B`, run with `transformers` on CPU. The model generates only the answer string; the code places it in the pydantic model and dumps the JSON.
5. **Evaluation** (`evaluate`): own recall@k, for iteration only. The official score comes from the moulinette.

Pipeline: `get_vllm_path` → `get_all_files` → `chunk_python_file` / `chunk_md_file` → `dump_chunks` → `index_chunks` (`bm25s`).

## Chunking strategy

- **Python** (`ast`): one pass over `ast.parse(code).body`. Each function, async function and class becomes its own chunk (never merged). All other top-level nodes accumulate into one contiguous "generic" chunk until the next function/class or end of file. Character offsets are computed from line starts combined with the AST line/column information.
- **Markdown**: split by headers (`#`) and code blocks (```` ``` ````).
- **Oversized units**: a unit larger than `max_chunk_size` is force-split with an overlap of 10% of `max_chunk_size`. No overlap otherwise.
- **`--max_chunk_size`**: default 2000 (the moulinette rejects longer sources). Values above 2000 are clamped to 2000; the minimum accepted value is 500.

## Retrieval method

BM25 through the `bm25s` library, with its default parameters: `bm25s.tokenize` with no stemming, no stopword removal and no identifier splitting. The index is saved to `data/processed/bm25_index`. At search time, `chunks.json` is reloaded as a list of `MinimalSource` in the same order used for indexing, and the integer indices returned by the retriever look up the matching chunk directly (path, offsets and content, without re-reading the source files).

## Performance analysis

Recall@k from the project's own `evaluate`:

| Dataset | @1 | @3 | @5 | @10 |
|---|---|---|---|---|
| docs | 0.56 | 0.81 | 0.86 | 0.89 |
| code | 0.33 | 0.47 | 0.53 | 0.62 |

Required thresholds at recall@5: docs ≥ 80%, code ≥ 50%. Both are met, and the project passes the reference moulinette.

Indexing the whole corpus took about 9.1 s on the development machine (limit: 5 minutes). This was not measured on the campus machines.

A match requires the same `file_path` and an IoU of at least 0.05 between the character ranges. Note the consequence for chunk size: with 2000-character chunks, a ground-truth source fully contained in a chunk only reaches the threshold if it spans at least 100 characters.

## Design decisions

- **Ingestion scope**: all files with a `.py` or `.md` extension in the vLLM repository, regardless of folder (`tests/`, `tools/`, `vllm/`, `docs/`, etc.), with no further filtering.
- **Chunk storage**: a single consolidated JSON at `data/processed/chunks/chunks.json` (not one file per source file), containing a list of chunk objects with `file_path`, `first_character_index`, `last_character_index`, `content` and `chunk_type`. Chosen for simplicity, easier pydantic validation and lower I/O overhead, within the 5-minute indexing limit.
- **`content` field on `MinimalSource`**: allowed by the subject (models may be expanded). It stores the chunk text alongside the offsets to avoid re-reading the vLLM sources when building the BM25 index.
- **`content` persistence**: persisted to `chunks.json`, not only kept in memory, because `index` and `search` are separate CLI invocations and in-memory data from `index` is lost by the time `search` runs.
- **BM25 indexing source**: `content` is extracted from each `MinimalSource` in the same order used for `bm25s.tokenize`/index; the original files are never re-read.
- **`StudentCLI` is not a pydantic model**: it is a stateless Fire dispatch layer with no data to validate. The subject requires pydantic only for the data models.
- **Argument validation**: done inside each command function, without pydantic models for arguments (simpler). Parsing errors raise `ParsingError` (or a subclass) from a dedicated `parsing_errors` module; the entry point only prints the message.
- **Inference**: vLLM could not be used as the inference engine on the development machine (AMD GPU under WSL, no platform detected), so `Qwen/Qwen3-0.6B` runs with `transformers` on CPU.
- **`evaluate` semantics**: the ground truth is the source of truth and is validated strictly (invalid JSON, items that are not `AnsweredQuestion`, empty `sources`, invalid character ranges, duplicate `question_id` → error). The student results are evaluated tolerantly: a ground-truth question missing from the results counts as recall 0 and stays in the denominator; extra questions are ignored. If the results file was produced with a `k` smaller than the requested recall@k, `evaluate` raises an error asking to re-run `search_dataset` with a larger `--k`.

## Challenges faced

No major difficulties. Markdown header handling needed a fix early on (a header line was being dropped when starting a new chunk).

## Resources

- Lewis et al., *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks* (2020): https://arxiv.org/abs/2005.11401
- Robertson & Zaragoza, *The Probabilistic Relevance Framework: BM25 and Beyond*
- `bm25s`: https://github.com/xhluca/bm25s
- Qwen3-0.6B model card: https://huggingface.co/Qwen/Qwen3-0.6B
- Hugging Face `transformers`, `pydantic`, Python Fire, `uv` and `tqdm` documentation

**Use of AI.** An AI assistant (Claude) was used to explain concepts (recall@k, IoU, interval intersection/union) and to clarify questions during implementation. The design of `evaluate` and the implementation were done by the author; AI output was checked and tested before use.
