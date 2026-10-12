import os
import json
from pathlib import Path
from src.models import MinimalSource


def dump_chunks(chunks: list[MinimalSource], output_file: str) -> None:
    output = Path(output_file)
    if output.exists():
        if os.access(output, os.W_OK):
            with open(output, mode="w") as file:
                json.dump([c.model_dump(mode='json') for c in chunks], file,
                          indent=4)
        else:
            raise PermissionError(
                output_file
            )
    else:
        output.parent.mkdir(mode=0o775, parents=True)
        with open(output, mode="w") as file:
            json.dump([c.model_dump(mode='json') for c in chunks], file,
                      indent=4)
