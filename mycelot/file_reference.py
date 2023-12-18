import datetime
import hashlib
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Optional

from mycelot.serializer import MetadataSerializer


@dataclass(slots=True)
class CatalogFileReference:
    name: str
    size: int
    md5: str
    is_dir: bool
    changed: datetime.datetime
    import_path: str
    catalog_path: Optional[str] = None


class FileReferenceRepository:
    """Manages creation and saving of file references to the file system."""

    def __init__(self, serializer: MetadataSerializer) -> None:
        self._serializer: MetadataSerializer = serializer

    def create_from_path(self, path: Path) -> CatalogFileReference:
        """Creates a new file reference from a path (an import path, not a
        catalog path).

        :param path: Import path to the file.
        :type path: Path
        :return: New file reference.
        :rtype: CatalogFileReference
        """
        return CatalogFileReference(
            name=path.name,
            size=path.stat().st_size,
            md5=hashlib.md5(path.read_bytes()).hexdigest(),
            is_dir=path.is_dir(),
            changed=datetime.datetime.fromtimestamp(path.stat().st_mtime),
            import_path=str(path.resolve())
        )

    def load_from_catalog_file(self, path: Path) -> CatalogFileReference:
        """Loads a file reference from an existing catalog reference.

        :param path: Path to the catalog metadata file.
        :type path: Path
        :return: File reference loaded from the catalog.
        :rtype: CatalogFileReference
        """
        with open(path) as file:
            data = self._serializer.deserialize(file.read())

        return CatalogFileReference(
            name=data["name"],
            size=data["size"],
            md5=data["md5"],
            is_dir=data["is_dir"],
            changed=datetime.datetime.fromisoformat(data["changed"]),
            import_path=data["import_path"]
        )

    def save_to_catalog_file(self, file: CatalogFileReference, path: Path) -> None:
        """Saves a catalog metadata file to the target path.

        :param file: Catalog file metadata to save.
        :type file: CatalogFileReference
        :param path: Path to new metadata file (in the .catalog folder)
        :type path: Path
        """

        with open(path, "w") as f:
            f.write(self._serializer.serialize(asdict(file)))
