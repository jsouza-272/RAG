import fire
from .errors import RagError
from .cli_handler import StudentCLI


def main() -> int:
    """
    Main entry point for the application.

    This function initializes the command-line interface using the
    `fire` library
    with the `StudentCLI` component. It handles any `RagError`
    exceptions that may
    occur during execution, printing the error message and returning a non-zero
    exit code to indicate failure.

    Returns:
        int: Returns 0 on successful execution, or 1 if a "
        "`RagError` is encountered.
    """

    try:
        fire.Fire(component=StudentCLI, name="uv run python3 -m src")
    except RagError as error:
        print(error)
        return 1
    return 0
