import fire
from .cli_handler import StudentCLI


def main():
    fire.Fire(component=StudentCLI, name="uv run python3 -m src")
