from pathlib import Path

from parsimonious.exceptions import ParseError

from mbotmake2.grammars.thumbnails import grammar
from mbotmake2.transformers.thumbnails import PNGImage, ThumbnailDecoder


def extractThumbnails(filename: Path, output_dir: Path) -> list[Path]:
    with open(filename, "r") as file:
        try:
            ast = grammar.match(file.read(5_000_000))
        except ParseError:
            print("Thumbnail not found. Skipping thumbnail generation...")
            return []

    decoder = ThumbnailDecoder()
    thumbnails: list[PNGImage] = decoder.visit(ast)

    thumbnail_paths: list[Path] = []
    for tn in thumbnails:
        h = tn.header
        filename = output_dir / f"thumbnail_{h.width}x{h.height}.png"
        with open(filename, "wb") as image_file:
            image_file.write(tn.payload)

        print(f"Saved {filename.name}")
        thumbnail_paths.append(filename)

    return thumbnail_paths
