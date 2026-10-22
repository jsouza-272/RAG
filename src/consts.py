INDEX_PATH = "data/processed/bm25_index"
CHUNKS_PATH = "data/processed/chunks/chunks.json"
INVALID_PATHS = [".venv", "__pycache__", ".git", ".mypy_cache"]
SYSTEM_PROMPT = (
    "You are a concise assistant. Answer the user question "
    "based ONLY on the provided Context. \n"
    "Rules:\n"
    "1. Rely only on the clear facts directly mentioned in the Context.\n"
    "2. Do not assume, extrapolate, or use outside knowledge.\n"
    "3. If the answer cannot be fully found in the Context, reply exactly "
    "with: 'I cannot find the answer in the provided documents.'\n"
    "4. Keep the response short, factual, and direct."
    " Do not use conversational filler.\n"
)
