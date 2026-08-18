import os
import fire
from .cli_handler import StudentCLI


def main():
    os.system("clear")
    fire.Fire(component=StudentCLI, name="uv run python3 -m src")
