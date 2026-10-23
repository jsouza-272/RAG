import fire
from .errors import RagError
from .cli_handler import StudentCLI


def main() -> int:
    try:
        fire.Fire(component=StudentCLI, name="uv run python3 -m src")
    except RagError as error:
        print(error)
        return 1
    return 0
