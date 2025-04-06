from pathlib import Path

from parsimonious.exceptions import IncompleteParseError

from mboxmake2.grammars.thumbnails import grammar


def extractThumbnails(
    filename: Path = Path("testcases/prusaslicer_gcode/cube.gcode"),
) -> None:
    with open(filename, "r") as file:
        try:
            ast = grammar.parse(file.read(5_000_000))
        except IncompleteParseError:
            pass

        print(ast)
