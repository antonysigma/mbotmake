from pathlib import Path

from mboxmake2.grammars.thumbnails import grammar
from mboxmake2.transformers.thumbnails import ImageMetadata, PNGImage, ThumbnailDecoder


def extractThumbnails(filename: Path) -> list[str]:
    with open(filename, "r") as file:
        ast = grammar.match(file.read(5_000_000))

    decoder = ThumbnailDecoder()
    thumbnails: list[PNGImage] = decoder.visit(ast)

    thumbnail_paths: list[Path] = []
    for t in thumbnails:
        h = t.header
        filename = Path(f"thumbnail_{h.width}x{h.height}.png")
        with open(filename, "wb") as image_file:
            image_file.write(t.payload)

        thumbnail_paths.append(filename)

    return thumbnail_paths
