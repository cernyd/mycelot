import xml.etree.ElementTree as ET
from typing import Protocol


class MetadataSerializer(Protocol):
    def serialize(self, metadata: dict) -> str:
        ...

    def deserialize(self, data: str) -> dict:
        ...

    @property
    def extension(self) -> str:
        """File extension for the serialized metadata."""
        ...


class XmlSerializer(MetadataSerializer):
    def serialize(self, metadata: dict) -> str:
        document = ET.Element("file")

        for key, value in metadata.items():
            ET.SubElement(document, key).text = str(value)

        ET.indent(document, space="    ")
        return ET.tostring(document, encoding="unicode")

    def deserialize(self, data: str) -> dict:
        document = ET.fromstring(data)

        result = {}
        for element in document:
            result[element.tag] = element.text

        return result

    @property
    def extension(self) -> str:
        return "xml"
