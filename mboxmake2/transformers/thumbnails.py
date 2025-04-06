from base64 import b64decode
from dataclasses import dataclass

from parsimonious.nodes import NodeVisitor


@dataclass
class ImageMetadata:
    width: int
    height: int
    size: int


class ThumbnailDecoder(NodeVisitor):
    def visit_Document(self, _, visited_children) -> list[bytes]:
        _, thumbnails = visited_children

        assert isinstance(thumbnails, list)
        assert isinstance(thumbnails[0], bytes)
        return thumbnails

    def visit_Thumbnail(self, _, visited_children) -> bytes:
        _, _, chunks, _ = visited_children

        assert isinstance(chunks, list)
        encoded = "".join(chunks)
        return b64decode(encoded)

    def visit_Payload(self, _, visited_children) -> str:
        _, chunk, _ = visited_children

        return chunk.text

    def generic_visit(self, node, visited_children):
        """The generic visit method."""
        return visited_children or node
