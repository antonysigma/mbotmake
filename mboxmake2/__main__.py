import json
from dataclasses import asdict
from itertools import islice

from mboxmake2.grammars.toolpath import grammar
from mboxmake2.metafile import generateMetajson
from mboxmake2.transformers.toolpath import ToolpathTransformer
from mboxmake2.types import Command, ExtruderType, MachineType
from mboxmake2.validate import collectPrinterSettings


def decodeGCodefile(
    filename: str = "testcases/prusaslicer_gcode/cube.gcode",
) -> ToolpathTransformer:
    with open(filename, "r") as file:
        transformer = ToolpathTransformer()
        while True:
            next_n_lines = list(islice(file, 4096))
            if not next_n_lines:
                break

            ast = grammar.parse("\n".join(next_n_lines))
            transformer.visit(ast)

    return transformer


transformer = decodeGCodefile()

# Checking toolpath
printer_settings = collectPrinterSettings(
    transformer.commands, transformer.z_transitions
)

# Write to meta json file
generateMetajson(
    printer_settings, MachineType.REPLICATORPlUS, ExtruderType.SMARTEXTRUDERPLUS
)

# Write to toolpath json file
with open("print.jsontoolpath", "w") as toolpathfile:
    toolpathfile.write("[\n")

    for cmd in transformer.commands:
        json.dump(asdict(cmd), toolpathfile)
        toolpathfile.write(",\n")

    json.dump(asdict(Command("comment", {"comment": "End of print"})), toolpathfile)
    toolpathfile.write("\n]\n")
