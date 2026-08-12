import fire
from .cli_handler import StudentCLI
from .indexer import get_vllm_path, get_all_files


def main():
    fire.Fire(component=StudentCLI, name="uv run python3 -m src")
    vllm_path = get_vllm_path()
    print(vllm_path)
    python_files = get_all_files(vllm_path, ".py")
    print(python_files)
    print("\033[38;2;255;0;255m", "="*200, "\033[0m")
    md_files = get_all_files(vllm_path, ".md")
    print(md_files)
