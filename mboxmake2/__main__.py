import json
from dataclasses import asdict
from itertools import islice

from mboxmake2.grammars.toolpath import grammar
from mboxmake2.transformers.toolpath import ToolpathTransformer
from mboxmake2.types import Command

with open("testcases/prusaslicer_gcode/cube.gcode", "r") as file:
    transformer = ToolpathTransformer()
    while True:
        next_n_lines = list(islice(file, 4096))
        if not next_n_lines:
            break

        ast = grammar.parse("\n".join(next_n_lines))
        transformer.visit(ast)

    del ast

    with open("print.jsontoolpath", "w") as toolpathfile:
        toolpathfile.write("[\n")

        for cmd in transformer.commands:
            json.dump(asdict(cmd), toolpathfile)
            toolpathfile.write(",\n")

        json.dump(asdict(Command("comment", {"comment": "End of print"})), toolpathfile)
        toolpathfile.write("\n]\n")

    # Checking toolpath
