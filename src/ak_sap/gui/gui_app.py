import subprocess
import sys
from pathlib import Path

import typer

app = typer.Typer()


@app.command()
def launch():
    streamlit_filepath: Path = (
        Path(__file__).parent.parent.parent.parent / "Start_Here.py"
    )
    subprocess.run(
        [f"{sys.executable}", "-m", "streamlit", "run", str(streamlit_filepath)]
    )
