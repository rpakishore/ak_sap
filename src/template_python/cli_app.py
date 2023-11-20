import typer
from rich import print
from typing import Optional
from pathlib import Path

from . import log, ic
ic.configureOutput(prefix=f'{Path(__file__).name} -> ')

app = typer.Typer()

@app.command()
def template_fn(template_str: str, template_bool: bool = False):
    """This is a sample function to be executed through the cli app
    """
    log.info('Called the `template_fn` function')
    ic(template_bool)
    ic(template_str)