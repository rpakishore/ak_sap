import json
from pathlib import Path
from typing import Optional

import typer

from ..utils import log

app = typer.Typer()


@app.command()
def template_fn():
    """This is a sample function to be executed through the cli app"""
    log.info("Called the `template_fn` function")
    doc_path: Path = Path(__file__).parent.parent.parent.parent / "documentation"

    replace_keyword = "# Initialize"

    layout = doc_path / "Layout.md"
    usage = doc_path / "Usage.ipynb"

    assert layout.is_file()
    assert usage.is_file()

    print("Layout docs found. Updating...", end="")

    with open(usage, "r") as f:
        data = json.load(f)

    with open(layout, "r") as f:
        contents = f.read().splitlines()
        contents = contents[: contents.index(replace_keyword)]

    for cell in data["cells"]:
        if cell.get("cell_type") == "markdown":
            contents.append("".join(cell.get("source"))[1:])
        elif cell.get("cell_type") == "code":
            _contents = "\nUsage Examples:\n\n```python\n"
            _contents += "".join(cell.get("source"))
            _contents += "\n```\n"
            contents.append(_contents)

    with open(layout, "w") as f:
        f.write("\n".join(contents))

    print("Done.")
