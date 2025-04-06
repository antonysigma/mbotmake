from pathlib import Path

from mboxmake2.grammars.thumbnails import grammar
from mboxmake2.transformers.thumbnails import PNGImage, ThumbnailDecoder


def extractThumbnails(
    filename: Path = Path("testcases/prusaslicer_gcode/cube.gcode"),
) -> None:
    with open(filename, "r") as file:
        ast = grammar.match(file.read(5_000_000))

    decoder = ThumbnailDecoder()
    thumbnails: list[PNGImage] = decoder.visit(ast)

    for i, t in enumerate(thumbnails):
        h = t.header
        with open(f"thumbnail_{h.width}x{h.height}.png", "wb") as image_file:
            image_file.write(t.payload)
