# mbotmake

A gcode to .makerbot conversion tool, compatible with Marlin gcode from OrcaSlicer.
And likely others.

**This is currently defaults to a Replicator Plus with a Smart Extruder**
I have added parameters to change which machine and extruder but I have only tested the <s>5th gen and a mini plus</s> Replicator+ with the settings the rest of the settings have been "extracted" from makerbot print.

# Usage

It's a Python script that generates a .makerbot file from a .gcode file that is
passed as an argument on the command line.

```shell
$ python3.12 -m mbotmake2 --help
usage: __main__.py [-h] [-m {Rep5,RepPlus,Mini5,MiniPlus}] [-e {SmartExt,SmartExtPlus,ToughExt,ExperimentalExt}] input

positional arguments:
  input                 Path to the input Gcode file

options:
  -h, --help            show this help message and exit
  -m {Rep5,RepPlus,Mini5,MiniPlus}, --machine {Rep5,RepPlus,Mini5,MiniPlus}
                        3D printer machine type
  -e {SmartExt,SmartExtPlus,ToughExt,ExperimentalExt}, --extruder {SmartExt,SmartExtPlus,ToughExt,ExperimentalExt}
```

Big notes for making your own config. Origin=middle, extruder absolute not relative.

<s>There is global variable at the top of mbotmake called DEBUG this will add each processed line as a "comment" into the jsontool path file I don't know if printing with all that in there will cause issues but it might so I recommend leaving it at False unless you are having weird issues and want to compare gcode-> jsontoolpath directly.</s>

## Installation

To be determined.

<s>There is now a github action that generates a mbotmake.exe for windows users that don't want to have to get python working for this. I hope to eventual split the configuration for the different printers out to property files and come up with a way to change which is being used</s>

<s>I'm adding my orcaslicer configuration for printer and process that seems to be working "well" I'm still having some issues but I think those a physical not gcode/makerbot code.</s>

# Contributing

## Download and configure the project

To setup the project for development:

1. Download and install `UV`, the Python package manager from https://docs.astral.sh/uv/#installation .

2. Install Python 3.12 through the UV tool: `uv python install 3.12`.

3. Clone this project to path `mbotmake/`;

4. From the terminal, cd into the path `mbotmake/`, and then setup the virtual environment `uv venv --python=3.12`; followed by `source .venv/bin/activate`;

5. Configure the project in the development mode: `uv pip install -U -e .[test]`;

## Unit testing

Now, the project is ready for testing. We can run the unit tests by:

```shell
cd mbotmake/
source .venv/bin/activate
pytest tests/
```

Which prints the following test summary:

```
============================ test session starts ==============================
platform linux -- Python 3.12.4, pytest-8.3.5, pluggy-1.5.0
rootdir: /home/antony/Projects/mbotmake
configfile: pyproject.toml
collected 14 items

tests/test_argparse.py ..                                                [ 14%]
tests/test_gcode_parsing.py .                                            [ 21%]
tests/test_thumbnail.py .                                                [ 28%]
tests/test_toolpath_parsing.py ..........                                [100%]

============================== 14 passed in 0.99s ==============================
```

## Check for Python syntax error

Verify the code with the linter tool  at `mbotmake/.venv/bin/ruff`, which should
print the following message:

```shell
cd mbotmake/
source .venv/bin/activate
ruff check
```

Which will print a message `All checks passed!` upon success. Otherwise, it
notifies us the syntax error:

```python
mbotmake2/transformers/toolpath.py:82:22: SyntaxError: Expected newline, found ','
   |
80 |         _, (coords,) = visited_children
81 |
82 |         match coords:,
   |                      ^
83 |             case Coords():
84 |                 self.generateMove2DCommand(coords)
   |
```

## Check for type and function argument error

Verify the code with the static type checking tool at `mbotmake/.venv/bin/mypy`:

```shell
cd mbotmake/
source .venv/bin/activate
mypy --ignore-missing-imports mbotmake2
```

Which will print a message `Success: no issues found in 13 source files` upon
success. Otherwise, it notifies us the function argument type error:

```python
mbotmake2/__main__.py:107: error:
Argument 3 to "collectPrinterSettings" has incompatible
type "int | None"; expected "int"  [arg-type]
```

## Packaging

Run the `uv build` command to generate the universal installation package for `mbotmake2`:

```shell
cd mbotmake/
source .venv/bin/activate
uv build
```

It should print the paths to the packages:

```
Successfully built dist/mbotmake2-0.0.1.tar.gz
Successfully built dist/mbotmake2-0.0.1-py3-none-any.whl
```

# NEW FEATURE
## Parameter machine/extruder control
There is now parameters to control which machine of the 5thgen/Plus family you are using and which extruder your using, These can be set in the post processing script in your slicer or when running in command line, You should be able to make a shortcut/batch script or something that would also use them for you.
*Note these are only partially tested many of the settings have been taken from Makerbot Print, Use at your own risk and report and issues or feedback please.*

|               |               |
| ------------- | ------------- |
| Replicator 5th gen | -m Rep5   |
| Replicator Mini (5th) | -m Mini5 |
| Replicator Plus | -RepPlus |
| Repliactor Mini Plus | -m MiniPlus |
| Smart Extruder | -e SmartExt |
| Smart Extruder Plus | -e SmartExtPlus |
| Smart Tough Extruder Plus | -e ToughExt |
| Experimental Smart Extruder Plus | -e ExperimentalExt |


## PrusaSlicer
Copied from [@sabesnait's](https://github.com/sabesnait) Fork of the original
Change these two settings in PrusaSlicer:
* Runs mbotmake automatically after exporting G-Code.<br><strong>[Print Settings] &rarr; [Output options] &rarr; [Post-processing scripts]:</strong><br>'[path to python] [.../]mbotmake -prusa -Rep5 -SmartExt'
* Generates the thumbnails for the Makerbot Replicator Gen5 display.<br><strong>[Printer Settings] &rarr; [General] &rarr; [G-code thumbnails]:</strong><br>
'55x40, 110x80, 320x200'

## OrcaSlicer
Change these two settings in OrcaSlicer:
* Runs mbotmake automatically after exporting G-Code.<br><strong>[Print Settings] &rarr; [Output options] &rarr; [Post-processing scripts]:</strong><br>'[path to python] [.../]mbotmake -orca -Rep5 -SmartExt'
* Generates the thumbnails for the Makerbot Replicator Gen5 display.<br><strong>[Printer Settings] &rarr; [General] &rarr; [G-code thumbnails]:</strong><br>
'55x40, 110x80, 320x200'

# TODO
~~Modify the script to handle all the different versions easily.~~ Now supported with Parameters

- [ ] Create Github Action rules to build the wheel package files for MacOS and Linux.

- [ ] Generate a standalone Windows exe app for Windows users.

- [ ] Add more test cases in the `tests/` folder.

- [ ] Write a nice and usable walkthrough for setting this up maybe even a video

- [ ] Make printer configs for all the different printers and different slicers (cura, prusa slicer, orca slicer)

- [ ] Figure out if there is a better way than trying to compile to exe that would mean its easier for people to use.

- [ ] More testing using different 5th gen and plus machines.

- [ ]Figure out how to do other nozzle sizes specifically 0.2mm or 0.6mm

