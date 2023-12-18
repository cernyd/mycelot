from pathlib import Path
from typing import Generator

import pytest

from mycelot.catalog import FileCatalog
from mycelot.exceptions.file_exists import FileExistsInCatalogException
from mycelot.file_reference import CatalogFileReference


@pytest.fixture
def catalog(tmp_path: Path) -> Generator[FileCatalog, None, None]:
    # Create a temporary directory for testing
    catalog_path = tmp_path / "test_catalog"
    catalog_path.mkdir()

    # Create a FileCatalog instance for testing
    file_catalog = FileCatalog(catalog_path)

    yield file_catalog


def test_catalog_path(catalog: FileCatalog) -> None:
    # Check if the catalog_path property returns the correct path
    assert catalog.catalog_path == catalog._path / ".catalog"


def test_add_file(catalog: FileCatalog, tmp_path: Path) -> None:
    # Create a temporary file for testing
    file_path = tmp_path / "test_file.txt"
    file_path.write_text("Test file content")

    # Add the file to the catalog
    file = catalog.add_file(file_path)

    # Check if the file is added to the catalog
    assert isinstance(file, CatalogFileReference)
    assert file.name == file_path.name


def test_add_existing_file(catalog: FileCatalog, tmp_path: Path) -> None:
    # Create a temporary file for testing
    file_path = tmp_path / "test_file.txt"
    file_path.write_text("Test file content")

    # Add the file to the catalog
    catalog.add_file(file_path)

    # Try to add the same file again
    with pytest.raises(FileExistsInCatalogException):
        catalog.add_file(file_path)


def test_load_files(catalog: FileCatalog, tmp_path: Path) -> None:
    # Create a temporary file for testing
    file_path = tmp_path / "test_file.txt"
    file_path.write_text("Test file content")

    # Add the file to the catalog
    catalog.add_file(file_path)

    # Check if the file is loaded in the catalog
    files = catalog._load_files()
    assert len(files) == 1
    assert isinstance(files[0], CatalogFileReference)
    assert files[0].name == file_path.name


def test_str(catalog: FileCatalog) -> None:
    # Check if the __str__ method returns the correct string representation
    assert str(catalog) == f"<FileCatalog path={catalog._path}>"
