import argparse
import json
import sys
import zipfile
from dataclasses import asdict
from itertools import islice
from pathlib import Path

from mboxmake2.extract_thumbnails import extractThumbnails
from mboxmake2.grammars.toolpath import grammar as toolpath_grammar
from mboxmake2.metafile import generateMetajson
from mboxmake2.transformers.toolpath import ToolpathTransformer
from mboxmake2.types import Command, ExtruderType, MachineType
from mboxmake2.validate import collectPrinterSettings


def decodeGCodefile(
    filename: Path = Path("testcases/prusaslicer_gcode/cube.gcode"),
) -> ToolpathTransformer:
    with open(filename, "r") as file:
        transformer = ToolpathTransformer()
        while True:
            next_n_lines = list(islice(file, 4096))
            if not next_n_lines:
                break

            ast = toolpath_grammar.parse("\n".join(next_n_lines))
            transformer.visit(ast)

    return transformer


def packageMBotFile(filename, temp_dir: str) -> None:
    with zipfile.ZipFile(filename, "w", compression=zipfile.ZIP_DEFLATED) as mbotfile:
        # for tn in tnNames:
        #    mbotfile.write(tn.format(temp), arcname=tn.strip("{}/"))

        mbotfile.write(f"{temp_dir}/meta.json", arcname="meta.json")
        mbotfile.write(f"{temp_dir}/print.jsontoolpath", arcname="print.jsontoolpath")


def parseArgs(argv: list[str]) -> tuple[Path, MachineType, ExtruderType]:
    parser = argparse.ArgumentParser()

    parser.add_argument("--SmartExtPlus", action="store_true")
    parser.add_argument("--ToughExt", action="store_true")
    parser.add_argument("input", type=Path)

    args = parser.parse_args(argv[1:])

    if not (args.SmartExtPlus ^ args.ToughExt):
        raise ValueError("Should not contain both extruder types")

    if args.SmartExtPlus:
        return (
            args.input,
            MachineType.REPLICATORPlUS,
            ExtruderType.SMARTEXTRUDERPLUS,
        )

    return parser.input, MachineType.REPLICATORPlUS, ExtruderType.TOUGHEXTRUDER


if __name__ == "__main__":
    input_file, machine_type, extruder_type = parseArgs(sys.argv)

    extractThumbnails(input_file)

    transformer = decodeGCodefile(input_file)

    # Checking toolpath
    printer_settings = collectPrinterSettings(
        transformer.commands, transformer.z_transitions
    )

    # Write to meta json file
    generateMetajson(printer_settings, machine_type, extruder_type)

    # Write to toolpath json file
    with open("print.jsontoolpath", "w") as toolpathfile:
        toolpathfile.write("[\n")

        for cmd in transformer.commands:
            json.dump(asdict(cmd), toolpathfile)
            toolpathfile.write(",\n")

        json.dump(asdict(Command("comment", {"comment": "End of print"})), toolpathfile)
        toolpathfile.write("\n]\n")

    packageMBotFile("output.makerbot", ".")
