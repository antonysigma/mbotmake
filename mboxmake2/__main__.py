import argparse
import json
import subprocess
import sys
import tempfile
import zipfile
from dataclasses import asdict
from itertools import islice
from pathlib import Path

from mboxmake2.extract_thumbnails import extractThumbnails
from mboxmake2.grammars.toolpath import grammar as toolpath_grammar
from mboxmake2.metafile import generateMetajson
from mboxmake2.progress import newProgressBar
from mboxmake2.transformers.toolpath import ToolpathTransformer
from mboxmake2.types import Command, ExtruderType, MachineType
from mboxmake2.validate import collectPrinterSettings


def countNewlines(file: Path) -> int:
    result = subprocess.check_output(["wc", "-l", file.as_posix()])
    return int(result.split()[0])


def decodeGCodefile(filename: Path) -> ToolpathTransformer:
    chunks = 4096

    progress_bar = newProgressBar(countNewlines(filename) // chunks * chunks + chunks)
    count = 0

    progress_bar.start()
    with open(filename, "r") as file:
        transformer = ToolpathTransformer()
        while True:
            next_n_lines = list(islice(file, chunks))
            if not next_n_lines:
                break

            ast = toolpath_grammar.parse("\n".join(next_n_lines))
            transformer.visit(ast)

            count += chunks
            progress_bar.update(count)

    progress_bar.finish()
    return transformer


def packageMBotFile(
    filename: Path, temp_dir: Path, thumbnail_paths: list[Path]
) -> None:
    with zipfile.ZipFile(filename, "w", compression=zipfile.ZIP_DEFLATED) as mbotfile:
        for tn in thumbnail_paths:
            mbotfile.write(tn, arcname=tn.name)

        mbotfile.write(temp_dir / "meta.json", arcname="meta.json")
        mbotfile.write(temp_dir / "print.jsontoolpath", arcname="print.jsontoolpath")


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

    with tempfile.TemporaryDirectory() as tmpdir_name:
        temp_dir = Path(tmpdir_name)

        thumbnail_paths = extractThumbnails(input_file, temp_dir)

        transformer = decodeGCodefile(input_file)

        # Checking toolpath
        printer_settings = collectPrinterSettings(
            transformer.commands, transformer.z_transitions
        )

        # Write to meta json file
        print("Generating meta.json...")
        generateMetajson(
            temp_dir / "meta.json", printer_settings, machine_type, extruder_type
        )

        # Write to toolpath json file
        print("Generating print.jsontoolpath...")
        with open(temp_dir / "print.jsontoolpath", "w") as toolpathfile:
            toolpathfile.write("[\n")

            for cmd in transformer.commands:
                json.dump(asdict(cmd), toolpathfile)
                toolpathfile.write(",\n")

            json.dump(
                asdict(Command("comment", {"comment": "End of print"})), toolpathfile
            )
            toolpathfile.write("\n]\n")

        output_file = input_file.with_suffix(".makerbot")
        print(f"Generating {output_file.name}...")
        packageMBotFile(output_file, temp_dir, thumbnail_paths)
