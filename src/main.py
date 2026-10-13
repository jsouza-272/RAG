import os
import fire
from .cli_handler import StudentCLI


def main() -> int:
    os.system("clear")
    fire.Fire(component=StudentCLI, name="uv run python3 -m src")
    return 0
