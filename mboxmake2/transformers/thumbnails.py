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
        _, _, first_thumbnail, other_thumbnails = visited_children

        assert isinstance(other_thumbnails, list)
        for _, new_thumbnail in other_thumbnails:
            first_thumbnail.append(new_thumbnail)

        return first_thumbnail

    def visit_Thumbnail(self, _, visited_children) -> bytes:
        _, chunks, _ = visited_children

        assert isinstance(chunks, list)
        encoded = "".join(chunks)
        return b64decode(encoded)

    def visit_Payload(self, _, visited_children) -> str:
        _, chunk, _ = visited_children

        return chunk.text

    def generic_visit(self, node, visited_children):
        """The generic visit method."""
        return visited_children or node
