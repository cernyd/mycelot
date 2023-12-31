import shutil
from pathlib import Path
from typing import List

from mycelot.exceptions.file_exists import FileExistsInCatalogException
from mycelot.file_reference import (CatalogFileReference,
                                    FileReferenceRepository)
from mycelot.serializer import XmlSerializer


class FileCatalog:
    """Contains logic for managing files in the catalog."""

    def __init__(self, path: Path) -> None:
        self._path = path

        for dir in self._path, self.catalog_path:
            dir.mkdir(exist_ok=True, parents=True)

        self._serializer = XmlSerializer()
        self._file_repository = FileReferenceRepository(self._serializer)
        self._files = self._load_files()

    def _load_files(self) -> List[CatalogFileReference]:
        files = []
        for file in self.catalog_path.glob(f"*.{self._serializer.extension}"):
            files.append(self._file_repository.load_from_catalog_file(file))

        return files

    @property
    def catalog_path(self) -> Path:
        return self._path / ".catalog"

    def add_file(self, path: Path) -> CatalogFileReference:
        """Adds a file to the catalog.

        :param path: Path to the file to add.
        :type path: Path
        :raises FileExistsInCatalogException: If the file already exists in the catalog.
        :return:
        :rtype: File
        """
        if path.is_absolute():
            catalog_dir = self._path
        else:
            catalog_dir = self._path / path.parent
            catalog_dir.mkdir(exist_ok=True, parents=True)

        target_path = catalog_dir / path.name

        if target_path.exists():
            raise FileExistsInCatalogException(str(path.resolve()))

        shutil.copy2(path, target_path)

        file = self._file_repository.create_from_path(path)
        file.catalog_path = str(target_path.relative_to(self._path))
        self._file_repository.save_to_catalog_file(file, self.catalog_path / f"{file.md5}.{self._serializer.extension}")

        return file

    def __str__(self) -> str:
        return f"<FileCatalog path={self._path}>"
