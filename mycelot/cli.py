from pathlib import Path

import click
from rich.console import Console

from mycelot.catalog import FileCatalog
from mycelot.exceptions.file_exists import FileExistsInCatalogException

console = Console()


path = Path(".")
catalog_dir = (path / "output" / ".mycelot").resolve()
IGNORE_DIRS = {".venv", ".git", "venv", ".mycelot", ".pytest_cache", ".mypy_cache", "output"}
IGNORE_SUFFIXES = {".pyc", ".pyo"}


catalog = FileCatalog(catalog_dir)

with console.status("[bold green]Indexing files..."):
    for file in path.glob("**/*"):
        if file.parts[0] in IGNORE_DIRS:
            continue

        if file.is_dir():
            continue

        last_suffix = file.suffixes[-1] if file.suffixes else ""
        if last_suffix in IGNORE_SUFFIXES:
            continue

        console.print(f"[bold white]{file.resolve()}[/bold white]")

        try:
            file_reference = catalog.add_file(file)
            console.print(f"[bold green]{file}[/bold green] -> {file_reference}")
        except FileExistsInCatalogException as e:
            console.print(f"[bold red]{e}[/bold red]")


@click.group()
def cli() -> None:
    pass


@cli.command()
def ls() -> None:
    print("List files")


@cli.command()
def add() -> None:
    print("Add files")


if __name__ == "__main__":
    cli()
