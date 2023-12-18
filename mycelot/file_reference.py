import datetime
import hashlib
from pathlib import Path

from mycelot.serializer import MetadataSerializer


class CatalogFileReference:
    def __init__(self, path: Path, serializer: MetadataSerializer) -> None:
        self._path = path
        self._serializer = serializer
        self._metadata: dict = self._load_metadata(self._path)

    @property
    def name(self) -> str:
        return self._metadata["name"]

    @property
    def metadata(self) -> dict:
        return self._metadata

    def _load_metadata(self, path: Path) -> dict:
        return {
            "name": path.name,
            "import_path": str(path.resolve()),
            "size": path.stat().st_size,
            "md5": hashlib.md5(path.read_bytes()).hexdigest(),
            "is_dir": path.is_dir(),
            "changed": datetime.datetime.fromtimestamp(path.stat().st_mtime),
        }

    def save(self) -> None:
        self._serializer.serialize(self._metadata)

    def __str__(self) -> str:
        return f"<File {self._metadata['name']} size={self._metadata['size']} md5={self._metadata['md5']}>"


class FileFactory:
    def __init__(self, serializer: MetadataSerializer) -> None:
        self._serializer: MetadataSerializer = serializer

    def from_path(self, path: Path) -> CatalogFileReference:
        return CatalogFileReference(path, self._serializer)
