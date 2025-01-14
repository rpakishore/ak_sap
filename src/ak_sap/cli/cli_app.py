import typer
from rich import print

from ..utils import log

app = typer.Typer()


@app.command()
def template_fn(template_str: str, template_bool: bool = False):
    """This is a sample function to be executed through the cli app"""
    log.info("Called the `template_fn` function")
    print("CLI app will be launched")
