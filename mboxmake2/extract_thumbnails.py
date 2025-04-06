from pathlib import Path

from parsimonious.exceptions import IncompleteParseError

from mboxmake2.grammars.thumbnails import grammar
from mboxmake2.transformers.thumbnails import ThumbnailDecoder


def extractThumbnails(
    filename: Path = Path("testcases/prusaslicer_gcode/cube.gcode"),
) -> None:
    with open(filename, "r") as file:
        ast = grammar.parse(file.read(5_000_000))

    decoder = ThumbnailDecoder()
    thumbnails = decoder.visit(ast)

    for i, t in enumerate(thumbnails):
        with open(f"{i}.png", "wb") as image_file:
            image_file.write(t)
