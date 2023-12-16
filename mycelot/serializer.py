from pathlib import Path
from typing import Protocol
import xml.etree.ElementTree as ET


class MetadataSerializer(Protocol):
    def serialize(self, metadata: dict) -> None:
        ...

    def deserialize(self, data: bytes) -> dict:
        ...


class XmlSerializer(MetadataSerializer):
    def __init__(self, sidecar_path: Path) -> None:
        self._sidecar_path = sidecar_path

    def serialize(self, metadata: dict) -> None:
        document = ET.Element("file")

        for key, value in metadata.items():
            ET.SubElement(document, key).text = str(value)

        ET.indent(document, space="    ")
        with open(self._sidecar_path / f"{metadata['name']}.xml", "w") as f:
            f.write(ET.tostring(document, encoding="unicode"))

    def deserialize(self, data: bytes) -> dict:
        raise NotImplementedError()
